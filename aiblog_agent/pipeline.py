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
        if item.link == primary.link:
            continue
        if len(out) >= limit:
            break
        out.append(item)
    return out


def _pick_publish_candidates(all_items: List[SourceItem], limit: int) -> List[SourceItem]:
    """Pick newest items while preferring domain diversity across a run."""
    selected: List[SourceItem] = []
    used_hosts: set[str] = set()

    for item in all_items:
        if len(selected) >= limit:
            break
        host = (urlparse(item.link).netloc or "").lower()
        if host and host in used_hosts:
            continue
        selected.append(item)
        if host:
            used_hosts.add(host)

    if len(selected) < limit:
        seen_links = {i.link for i in selected}
        for item in all_items:
            if len(selected) >= limit:
                break
            if item.link in seen_links:
                continue
            selected.append(item)
            seen_links.add(item.link)

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
