from __future__ import annotations

import base64
from dataclasses import dataclass
from typing import Any, Dict

import requests

from .config import Settings
from .writer import GeneratedPost


@dataclass(frozen=True)
class WordPressResult:
    post_id: int
    url: str


class WordPressPublisher:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def publish(self, post: GeneratedPost) -> WordPressResult:
        if not self.settings.wordpress_site_url:
            raise RuntimeError("WORDPRESS_SITE_URL is missing")
        if not self.settings.wordpress_username or not self.settings.wordpress_app_password:
            raise RuntimeError("WordPress credentials are missing")

        endpoint = f"{self.settings.wordpress_site_url}/wp-json/wp/v2/posts"
        creds = f"{self.settings.wordpress_username}:{self.settings.wordpress_app_password}".encode("utf-8")
        token = base64.b64encode(creds).decode("ascii")

        payload: Dict[str, Any] = {
            "title": post.title,
            "slug": post.slug,
            "content": post.html_content,
            "excerpt": post.excerpt,
            "status": self.settings.wordpress_default_status,
        }
        if self.settings.wordpress_default_category:
            try:
                payload["categories"] = [int(self.settings.wordpress_default_category)]
            except ValueError:
                pass

        resp = requests.post(
            endpoint,
            headers={
                "Authorization": f"Basic {token}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=60,
        )
        resp.raise_for_status()
        data = resp.json()
        return WordPressResult(post_id=int(data["id"]), url=data["link"])
