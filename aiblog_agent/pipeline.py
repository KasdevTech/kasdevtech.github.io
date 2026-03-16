from __future__ import annotations

from typing import List
from urllib.parse import urlparse

from .config import Settings
from .ghpages import GitHubPagesPublisher
from .local_publish import LocalPublisher
from .linkedin import LinkedInPublisher
from .sources import SourceItem, collect_source_items
from .state import init_db, mark_source_published, was_source_published
from .wordpress import WordPressPublisher
from .writer import BlogWriter


def _pick_related(all_items: List[SourceItem], primary: SourceItem, limit: int = 3) -> List[SourceItem]:
    out: List[SourceItem] = []

    for item in all_items:
        if item.link == primary.link or item.section != primary.section:
            continue
        if len(out) >= limit:
            break
        out.append(item)

    for item in all_items:
        if item.link == primary.link or item in out:
            continue
        if len(out) >= limit:
            break
        out.append(item)
    return out


def _scenario_score(item: SourceItem) -> int:
    text = f"{item.title}\n{item.summary}\n{item.source}".lower()

    azure_terms = {
        "outage",
        "incident",
        "issue",
        "issues",
        "troubleshooting",
        "troubleshoot",
        "degradation",
        "latency",
        "downtime",
        "migration",
        "security",
        "cost",
        "network",
        "monitor",
        "monitoring",
        "app service",
        "aks",
        "application gateway",
        "private endpoint",
        "virtual network",
        "entra",
        "performance",
        "operations",
        "production",
        "failure",
        "reliability",
    }
    ai_terms = {
        "implementation",
        "deploy",
        "deployment",
        "production",
        "workflow",
        "architecture",
        "build",
        "evaluation",
        "guardrail",
        "rag",
        "agent",
        "orchestration",
        "inference",
        "latency",
        "cost",
        "benchmark",
        "enterprise",
        "integration",
    }

    score = 0
    if item.section == "azure":
        score += sum(1 for term in azure_terms if term in text)
    elif item.section == "ai":
        score += sum(1 for term in ai_terms if term in text)
    else:
        score += sum(1 for term in {"security", "automation", "migration", "performance", "operations"} if term in text)
    return score


def _sorted_section_items(all_items: List[SourceItem], section: str) -> List[SourceItem]:
    section_items = [item for item in all_items if item.section == section]
    return sorted(
        section_items,
        key=lambda item: (_scenario_score(item), item.published_at),
        reverse=True,
    )


def _pick_publish_candidates(all_items: List[SourceItem], limit: int) -> List[SourceItem]:
    """Pick newest items while favoring Azure first, AI second, then other cloud sections."""
    selected: List[SourceItem] = []
    used_hosts: set[str] = set()
    used_links: set[str] = set()

    preferred_sections = ["azure", "ai", "devops", "terraform", "cloud"]
    section_order: List[str] = []
    for section in preferred_sections:
        if any(item.section == section for item in all_items):
            section_order.append(section)
    for item in all_items:
        if item.section not in section_order:
            section_order.append(item.section)

    for section in section_order:
        if len(selected) >= limit:
            break
        for item in _sorted_section_items(all_items, section):
            if item.link in used_links:
                continue
            host = (urlparse(item.link).netloc or "").lower()
            if host and host in used_hosts:
                continue
            selected.append(item)
            used_links.add(item.link)
            if host:
                used_hosts.add(host)
            break

    for item in all_items:
        if len(selected) >= limit:
            break
        if item.link in used_links:
            continue
        host = (urlparse(item.link).netloc or "").lower()
        if host and host in used_hosts:
            continue
        selected.append(item)
        used_links.add(item.link)
        if host:
            used_hosts.add(host)

    if len(selected) < limit:
        for item in all_items:
            if len(selected) >= limit:
                break
            if item.link in used_links:
                continue
            selected.append(item)
            used_links.add(item.link)

    return selected


def run_once(settings: Settings) -> None:
    init_db(settings.published_state_file)

    all_items = collect_source_items(settings)
    if not all_items:
        print("No recent source items found; nothing to publish.")
        return

    writer = BlogWriter(settings)
    wordpress = WordPressPublisher(settings) if settings.publish_wordpress else None
    linkedin = LinkedInPublisher(settings)
    ghpages = GitHubPagesPublisher(settings)
    local = LocalPublisher(settings.local_output_dir)

    publish_candidates = _pick_publish_candidates(all_items, settings.posts_per_run * 4)

    published = 0
    for primary in publish_candidates:
        if published >= settings.posts_per_run:
            break
        if was_source_published(primary.link, settings.published_state_file):
            continue

        topic_hint = primary.title
        related = _pick_related(all_items, primary)
        generated = writer.generate(primary=primary, related=related, topic_hint=topic_hint)

        wp_url = ""
        if wordpress is not None:
            wp_result = wordpress.publish(generated)
            wp_url = wp_result.url
            mark_source_published(primary.link, wp_url, settings.published_state_file)
        else:
            mark_source_published(primary.link, "local-only", settings.published_state_file)

        local_result = local.publish(generated, wp_url)
        print(f"Local post written: {local_result.md_path}")
        print(f"Local HTML written: {local_result.html_path}")

        gh_result = ghpages.publish(generated, wp_url)
        if gh_result:
            print(f"GitHub Pages post written: {gh_result.file_path}")
            if gh_result.commit_sha:
                print(f"GitHub Pages commit: {gh_result.commit_sha}")

        if settings.linkedin_enabled and wp_url:
            try:
                linkedin.publish(generated.linkedin_text, wp_url)
            except Exception as exc:
                print(f"LinkedIn publish failed for {wp_url}: {exc}")

        published += 1
        destination = wp_url or local_result.md_path
        print(f"Published #{published}: {generated.title} -> {destination}")

    if published == 0:
        print("All eligible sources are already published or filtered out.")
