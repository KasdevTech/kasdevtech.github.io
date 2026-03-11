from __future__ import annotations

import datetime as dt
from dataclasses import dataclass
from pathlib import Path

from .writer import GeneratedPost


@dataclass(frozen=True)
class LocalPublishResult:
    html_path: str
    md_path: str


class LocalPublisher:
    def __init__(self, output_dir: str = "generated_posts") -> None:
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def publish(self, post: GeneratedPost, canonical_url: str = "") -> LocalPublishResult:
        ts = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
        base = f"{ts}-{post.slug}"

        html_path = self.output_dir / f"{base}.html"
        md_path = self.output_dir / f"{base}.md"

        html_doc = (
            "<!doctype html>\n"
            "<html><head><meta charset=\"utf-8\"><title>"
            f"{post.title}"
            "</title></head><body>"
            f"<h1>{post.title}</h1>"
            f"<p><em>{post.excerpt}</em></p>"
            + (f"<p>Canonical: <a href=\"{canonical_url}\">{canonical_url}</a></p>" if canonical_url else "")
            + post.html_content
            + "</body></html>\n"
        )
        html_path.write_text(html_doc, encoding="utf-8")

        md_doc = (
            f"# {post.title}\n\n"
            f"{post.excerpt}\n\n"
            + (f"Canonical: {canonical_url}\n\n" if canonical_url else "")
            +
            f"{post.html_content}\n"
        )
        md_path.write_text(md_doc, encoding="utf-8")

        return LocalPublishResult(html_path=str(html_path), md_path=str(md_path))
