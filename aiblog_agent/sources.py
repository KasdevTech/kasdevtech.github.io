from __future__ import annotations

import datetime as dt
from dataclasses import dataclass
from email.utils import parsedate_to_datetime
from typing import Iterable, List
from urllib.parse import quote_plus, urlparse

import feedparser

from .config import Settings, resolved_rss_feeds


@dataclass(frozen=True)
class SourceItem:
    source: str
    title: str
    link: str
    summary: str
    published_at: dt.datetime
    section: str


def _parse_feed_timestamp(entry: dict) -> dt.datetime | None:
    candidates = [entry.get("published"), entry.get("updated")]
    for raw in candidates:
        if not raw:
            continue
        try:
            parsed = parsedate_to_datetime(raw)
            if parsed.tzinfo is None:
                parsed = parsed.replace(tzinfo=dt.timezone.utc)
            return parsed.astimezone(dt.timezone.utc)
        except Exception:
            continue
    return None


def _google_news_rss(topic: str) -> str:
    query = quote_plus(f'"{topic}" (ai OR llm OR agent OR mcp OR langchain OR azure OR cloud) when:1d')
    return f"https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en"


def _match_topic(text: str, topics: Iterable[str]) -> bool:
    low = text.lower()
    return any(t.lower() in low for t in topics)


def _looks_non_technical(text: str) -> bool:
    bad_terms = {
        "music",
        "song",
        "rapper",
        "celebrity",
        "movie",
        "film",
        "trailer",
        "gossip",
        "sports",
        "match",
        "score",
        "lottery",
        "dating",
    }
    low = text.lower()
    return any(term in low for term in bad_terms)


def _is_trusted_news_domain(link: str) -> bool:
    host = urlparse(link).netloc.lower()
    trusted = (
        "microsoft.com",
        "azure.microsoft.com",
        "devblogs.microsoft.com",
        "learn.microsoft.com",
        "techcommunity.microsoft.com",
        "openai.com",
        "anthropic.com",
        "ai.google.dev",
        "googleblog.com",
        "blog.langchain.dev",
        "langchain.com",
        "langgraph.dev",
        "llamaindex.ai",
        "huggingface.co",
        "github.blog",
        "github.com",
        "aws.amazon.com",
        "cloud.google.com",
        "databricks.com",
        "hashicorp.com",
        "kubernetes.io",
        "docker.com",
        "cloudflare.com",
        "vercel.com",
        "mongodb.com",
        "redis.io",
        "elastic.co",
        "datadoghq.com",
        "prometheus.io",
        "grafana.com",
        "arstechnica.com",
        "infoq.com",
        "thenewstack.io",
        "techcrunch.com",
        "theverge.com",
        "venturebeat.com",
    )
    return any(host.endswith(d) for d in trusted)


def classify_section(title: str, summary: str, link: str, source: str) -> str:
    text = f"{title}\n{summary}\n{source}".lower()
    host = urlparse(link).netloc.lower()

    terraform_terms = {
        "terraform",
        "tfstate",
        "hashicorp",
        "iac",
        "infrastructure as code",
    }
    devops_terms = {
        "devops",
        "github actions",
        "github",
        "ci/cd",
        "pipeline",
        "pipelines",
        "docker",
        "kubernetes",
        "aks",
        "helm",
        "container",
        "observability",
        "datadog",
        "prometheus",
        "grafana",
        "sre",
        "platform engineering",
    }
    azure_terms = {
        "azure",
        "entra",
        "microsoft fabric",
        "azure databricks",
        "azure openai",
        "app service",
        "application gateway",
        "virtual network",
        "vnet",
        "private endpoint",
        "azure sql",
        "azure storage",
        "azure kubernetes",
        "azure devops",
    }
    ai_terms = {
        "ai",
        "llm",
        "agent",
        "agents",
        "mcp",
        "model context protocol",
        "langchain",
        "langgraph",
        "llamaindex",
        "openai",
        "anthropic",
        "gemini",
        "bedrock",
        "vertex ai",
        "copilot",
        "rag",
        "prompt",
    }

    if any(term in text for term in terraform_terms) or "hashicorp" in host:
        return "terraform"
    if any(term in text for term in devops_terms) or host.endswith(("kubernetes.io", "github.blog", "docker.com")):
        return "devops"
    if any(term in text for term in azure_terms) or host.endswith(("microsoft.com", "azure.microsoft.com")):
        return "azure"
    if any(term in text for term in ai_terms):
        return "ai"
    if host.endswith(("aws.amazon.com", "cloud.google.com", "databricks.com", "cloudflare.com")):
        return "cloud"
    return "cloud"


def collect_source_items(settings: Settings) -> List[SourceItem]:
    now = dt.datetime.now(dt.timezone.utc)
    threshold = now - dt.timedelta(hours=settings.lookback_hours)

    feeds: List[str] = list(resolved_rss_feeds(settings))
    feeds.extend(_google_news_rss(topic) for topic in settings.topics)

    items: List[SourceItem] = []
    for feed_url in feeds:
        parsed = feedparser.parse(feed_url)
        source_title = parsed.feed.get("title", feed_url)
        for entry in parsed.entries:
            published_at = _parse_feed_timestamp(entry)
            if published_at is None or published_at < threshold:
                continue

            title = (entry.get("title") or "").strip()
            link = (entry.get("link") or "").strip()
            summary = (entry.get("summary") or "").strip()
            if not title or not link:
                continue
            combined_text = f"{title}\n{summary}"
            if not _match_topic(combined_text, settings.topics):
                continue
            if _looks_non_technical(combined_text):
                continue
            source_info = entry.get("source", {}) if isinstance(entry.get("source", {}), dict) else {}
            publisher_href = (source_info.get("href") or "").strip()
            if "news.google.com" in link and publisher_href and not _is_trusted_news_domain(publisher_href):
                continue
            items.append(
                SourceItem(
                    source=source_title,
                    title=title,
                    link=link,
                    summary=summary,
                    published_at=published_at,
                    section=classify_section(title=title, summary=summary, link=link, source=source_title),
                )
            )

    # Deduplicate by URL and sort newest first.
    dedup: dict[str, SourceItem] = {}
    for item in sorted(items, key=lambda i: i.published_at, reverse=True):
        dedup.setdefault(item.link, item)

    return list(dedup.values())
