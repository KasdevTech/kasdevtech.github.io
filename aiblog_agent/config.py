from __future__ import annotations

import os
from dataclasses import dataclass
from typing import List

from dotenv import load_dotenv

load_dotenv()


def _get_bool(name: str, default: bool) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


def _get_list(name: str, default: List[str]) -> List[str]:
    raw = os.getenv(name, "")
    if not raw.strip():
        return default
    return [item.strip() for item in raw.split(",") if item.strip()]


@dataclass(frozen=True)
class Settings:
    openai_api_key: str
    openai_model: str
    openai_base_url: str

    wordpress_site_url: str
    wordpress_username: str
    wordpress_app_password: str
    wordpress_default_status: str
    wordpress_default_category: str

    linkedin_enabled: bool
    linkedin_access_token: str
    linkedin_author_urn: str

    timezone: str
    run_hour_24: int
    run_minute: int
    posts_per_run: int
    lookback_hours: int

    topics: List[str]
    extra_rss_feeds: List[str]
    publish_wordpress: bool
    local_output_dir: str

    github_pages_repo_path: str
    github_pages_posts_dir: str
    github_pages_auto_commit: bool
    github_pages_auto_push: bool
    published_state_file: str


DEFAULT_TOPICS = [
    "AI",
    "MCP",
    "Model Context Protocol",
    "LangChain",
    "LangGraph",
    "LlamaIndex",
    "Azure AI",
    "Azure Databricks",
    "Microsoft Fabric",
    "Azure OpenAI",
    "GitHub Copilot",
    "OpenAI",
    "Anthropic",
    "Gemini",
    "Vertex AI",
    "Google Cloud AI",
    "Google Cloud",
    "AWS AI",
    "Amazon Bedrock",
    "SageMaker",
    "Cloudflare AI",
    "Kubernetes",
    "Docker",
    "Terraform",
    "DevSecOps",
    "Observability",
    "Datadog",
    "Prometheus",
]


DEFAULT_RSS_FEEDS = [
    "https://azure.microsoft.com/en-us/blog/feed/",
    "https://devblogs.microsoft.com/feed/",
    "https://blog.langchain.dev/rss/",
    "https://openai.com/news/rss.xml",
    "https://www.anthropic.com/news/rss.xml",
    "https://cloud.google.com/blog/products/ai-machine-learning/rss/",
    "https://aws.amazon.com/blogs/machine-learning/feed/",
    "https://aws.amazon.com/blogs/devops/feed/",
    "https://www.databricks.com/blog/feed",
    "https://www.hashicorp.com/blog/products/terraform/feed.xml",
    "https://kubernetes.io/feed.xml",
    "https://github.blog/changelog/feed/",
]


def load_settings() -> Settings:
    return Settings(
        openai_api_key=os.getenv("OPENAI_API_KEY", ""),
        openai_model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
        openai_base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/"),
        wordpress_site_url=os.getenv("WORDPRESS_SITE_URL", "").rstrip("/"),
        wordpress_username=os.getenv("WORDPRESS_USERNAME", ""),
        wordpress_app_password=os.getenv("WORDPRESS_APP_PASSWORD", ""),
        wordpress_default_status=os.getenv("WORDPRESS_DEFAULT_STATUS", "publish"),
        wordpress_default_category=os.getenv("WORDPRESS_DEFAULT_CATEGORY", ""),
        linkedin_enabled=_get_bool("LINKEDIN_ENABLED", True),
        linkedin_access_token=os.getenv("LINKEDIN_ACCESS_TOKEN", ""),
        linkedin_author_urn=os.getenv("LINKEDIN_AUTHOR_URN", ""),
        timezone=os.getenv("TIMEZONE", "Asia/Kolkata"),
        run_hour_24=int(os.getenv("RUN_HOUR_24", "19")),
        run_minute=int(os.getenv("RUN_MINUTE", "0")),
        posts_per_run=int(os.getenv("POSTS_PER_RUN", "2")),
        lookback_hours=int(os.getenv("LOOKBACK_HOURS", "36")),
        topics=_get_list("TOPICS", DEFAULT_TOPICS),
        extra_rss_feeds=_get_list("EXTRA_RSS_FEEDS", []),
        publish_wordpress=_get_bool("PUBLISH_WORDPRESS", True),
        local_output_dir=os.getenv("LOCAL_OUTPUT_DIR", "generated_posts"),
        github_pages_repo_path=os.getenv("GITHUB_PAGES_REPO_PATH", ""),
        github_pages_posts_dir=os.getenv("GITHUB_PAGES_POSTS_DIR", "_posts"),
        github_pages_auto_commit=_get_bool("GITHUB_PAGES_AUTO_COMMIT", False),
        github_pages_auto_push=_get_bool("GITHUB_PAGES_AUTO_PUSH", False),
        published_state_file=os.getenv("PUBLISHED_STATE_FILE", ""),
    )


def resolved_rss_feeds(settings: Settings) -> List[str]:
    return DEFAULT_RSS_FEEDS + settings.extra_rss_feeds
