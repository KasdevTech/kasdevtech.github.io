from __future__ import annotations

import datetime as dt
import subprocess
from dataclasses import dataclass
from pathlib import Path

from .config import Settings
from .writer import GeneratedPost


@dataclass(frozen=True)
class GitHubPagesResult:
    file_path: str
    commit_sha: str | None


class GitHubPagesPublisher:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def publish(self, post: GeneratedPost, wordpress_url: str) -> GitHubPagesResult | None:
        repo_path = self.settings.github_pages_repo_path
        if not repo_path:
            return None

        root = Path(repo_path).expanduser().resolve()
        content_root = root / self.settings.github_pages_posts_dir.strip().strip("/")
        section_dir = _section_directory(post.section)
        posts_dir = content_root / section_dir
        posts_dir.mkdir(parents=True, exist_ok=True)

        today = dt.date.today()
        filename = f"{today.isoformat()}-{post.slug}.md"
        post_path = posts_dir / filename

        safe_title = _yaml_escape(post.title)
        safe_excerpt = _yaml_escape(post.excerpt)
        published_at = dt.datetime.now(dt.timezone.utc).isoformat()
        front_matter = (
            "---\n"
            f"title: \"{safe_title}\"\n"
            f"date: {published_at}\n"
            f"lastmod: {published_at}\n"
            "draft: false\n"
            f"slug: \"{post.slug}\"\n"
            f"url: \"/{post.section}/{post.slug}/\"\n"
            f"categories: [{', '.join(post.categories)}]\n"
            f"summary: \"{safe_excerpt}\"\n"
            f"excerpt: \"{safe_excerpt}\"\n"
            f"canonical_url: \"{wordpress_url}\"\n"
            "---\n\n"
        )

        body = (
            f"{front_matter}"
            "This article was auto-published by AI Blog Generation Agent.\n\n"
            f"Canonical WordPress URL: {wordpress_url}\n\n"
            f"{post.html_content}\n"
        )
        post_path.write_text(body, encoding="utf-8")

        commit_sha = None
        if self.settings.github_pages_auto_commit:
            rel_post_path = post_path.relative_to(root)
            subprocess.run(["git", "-C", str(root), "add", str(rel_post_path)], check=True)
            state_file = self.settings.published_state_file.strip()
            if state_file:
                state_path = Path(state_file).expanduser().resolve()
                if state_path.exists() and str(state_path).startswith(str(root)):
                    rel_state = state_path.relative_to(root)
                    subprocess.run(["git", "-C", str(root), "add", str(rel_state)], check=True)
            subprocess.run(
                ["git", "-C", str(root), "commit", "-m", f"Add post: {post.title}"],
                check=True,
            )
            if self.settings.github_pages_auto_push:
                subprocess.run(["git", "-C", str(root), "push"], check=True)
            commit_sha = (
                subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"])
                .decode("utf-8")
                .strip()
            )

        return GitHubPagesResult(file_path=str(post_path), commit_sha=commit_sha)


def _yaml_escape(text: str) -> str:
    return text.replace("\\", "\\\\").replace('"', '\\"')


def _section_directory(section: str) -> str:
    mapping = {
        "ai": "AI",
        "azure": "Azure",
        "devops": "Devops",
        "terraform": "Terraform",
        "cloud": "AI",
    }
    return mapping.get(section, "AI")
