from __future__ import annotations

import requests

from .config import Settings


class LinkedInPublisher:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def publish(self, text: str, article_url: str) -> None:
        if not self.settings.linkedin_enabled:
            return
        if not self.settings.linkedin_access_token or not self.settings.linkedin_author_urn:
            raise RuntimeError("LinkedIn is enabled but LINKEDIN_ACCESS_TOKEN or LINKEDIN_AUTHOR_URN is missing")

        endpoint = "https://api.linkedin.com/v2/ugcPosts"
        body = {
            "author": self.settings.linkedin_author_urn,
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {"text": f"{text}\n\nRead more: {article_url}"},
                    "shareMediaCategory": "ARTICLE",
                    "media": [
                        {
                            "status": "READY",
                            "description": {"text": "Latest AI update"},
                            "originalUrl": article_url,
                            "title": {"text": "New blog post"},
                        }
                    ],
                }
            },
            "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"},
        }
        resp = requests.post(
            endpoint,
            headers={
                "Authorization": f"Bearer {self.settings.linkedin_access_token}",
                "Content-Type": "application/json",
                "X-Restli-Protocol-Version": "2.0.0",
            },
            json=body,
            timeout=60,
        )
        resp.raise_for_status()
