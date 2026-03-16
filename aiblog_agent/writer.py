from __future__ import annotations

import json
import re
from datetime import date
from dataclasses import dataclass
from typing import Iterable, List
from urllib.parse import urlparse

import requests
from tenacity import retry, stop_after_attempt, wait_exponential

from .config import Settings
from .sources import SourceItem


@dataclass(frozen=True)
class GeneratedPost:
    title: str
    slug: str
    html_content: str
    excerpt: str
    linkedin_text: str
    section: str
    categories: List[str]


class BlogWriter:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=8))
    def _chat(self, system: str, user: str) -> str:
        if not self.settings.openai_api_key and not _is_local_ollama_url(self.settings.openai_base_url):
            raise RuntimeError("OPENAI_API_KEY is missing")

        url = f"{self.settings.openai_base_url}/chat/completions"
        headers = {"Content-Type": "application/json"}
        if self.settings.openai_api_key:
            headers["Authorization"] = f"Bearer {self.settings.openai_api_key}"
        payload = {
            "model": self.settings.openai_model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "temperature": 0.4,
            "max_tokens": 1800,
        }
        resp = requests.post(url, headers=headers, json=payload, timeout=90)
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"]

    def generate(self, primary: SourceItem, related: Iterable[SourceItem], topic_hint: str) -> GeneratedPost:
        rel = list(related)
        if not self.settings.openai_api_key and not _is_local_ollama_url(self.settings.openai_base_url):
            return _fallback_generate(primary, rel, topic_hint)

        rel_lines: List[str] = []
        for idx, item in enumerate([primary] + rel, start=1):
            rel_lines.append(
                f"{idx}. TITLE: {item.title}\nSOURCE: {item.source}\nURL: {item.link}\nSUMMARY: {item.summary[:800]}"
            )

        system = (
            "You are a senior technical blog editor. Produce factual, high-quality HTML blog drafts "
            "for a developer audience. Do not invent facts. Use only provided sources."
        )
        today_iso = date.today().isoformat()
        user = f"""
Generate one technical blog post about: {topic_hint}

Use these sources:
{chr(10).join(rel_lines)}

Return JSON only with keys:
- title (string)
- slug (kebab-case ascii)
- excerpt (max 220 chars)
- html_content (valid HTML fragment with h2/h3, bullets, code block if relevant, and a 'Sources' section linking all used URLs)
- linkedin_text (short post with 3-5 hashtags and call-to-action)

Constraints:
- 1000 to 1600 words.
- Tone: practical, clear, not hype.
- Include one section specifically for enterprise impact.
- Keep the article aligned to this primary section: {primary.section}.
- Avoid Azure-only bias unless the source itself is Azure-specific; cover multi-cloud implications where relevant.
- Mention date context as "As of {today_iso}" near the intro.
""".strip()

        try:
            raw = self._chat(system, user)
            data = _extract_json(raw)
            return GeneratedPost(
                title=data["title"].strip(),
                slug=_slugify(data["slug"] or data["title"]),
                html_content=data["html_content"].strip(),
                excerpt=data["excerpt"].strip(),
                linkedin_text=data["linkedin_text"].strip(),
                section=primary.section,
                categories=_categories_for_section(primary.section),
            )
        except Exception as exc:
            print(f"LLM output parsing failed; using fallback template. Error: {exc}")
            return _fallback_generate(primary, rel, topic_hint)


def _slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"\s+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text[:100].strip("-")


def _extract_json(raw: str) -> dict:
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.strip("`")
        raw = raw.replace("json", "", 1).strip()

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        start = raw.find("{")
        end = raw.rfind("}")
        if start == -1 or end == -1:
            raise RuntimeError("Model output is not valid JSON")
        data = json.loads(raw[start : end + 1])

    required = {"title", "slug", "excerpt", "html_content", "linkedin_text"}
    missing = required - set(data.keys())
    if missing:
        raise RuntimeError(f"Missing keys from model output: {sorted(missing)}")
    return data


def _fallback_generate(primary: SourceItem, related: List[SourceItem], topic_hint: str) -> GeneratedPost:
    title = f"{topic_hint}: Key Updates for Builders"
    slug = _slugify(title)
    excerpt = (
        f"Practical summary of the latest updates around {topic_hint}, with implications for engineering teams."
    )[:220]

    sources = [primary] + related[:3]
    bullets = []
    for item in sources:
        bullets.append(
            f"<li><a href=\"{item.link}\">{item.title}</a> "
            f"(<em>{item.source}</em>, {item.published_at.date().isoformat()})</li>"
        )

    html_content = (
        f"<p>As of {date.today().isoformat()}, here are the most relevant updates for {topic_hint}.</p>"
        "<h2>What Happened</h2>"
        "<ul>"
        + "".join(bullets)
        + "</ul>"
        "<h2>Why It Matters for Enterprise Teams</h2>"
        "<p>These announcements indicate faster adoption of AI agents, stronger ecosystem integration, "
        "and increasing need for governance, observability, and evaluation workflows in production.</p>"
        "<h2>Implementation Notes</h2>"
        "<ul>"
        "<li>Prioritize one pilot use case with measurable KPIs.</li>"
        "<li>Use retrieval and evaluation loops before broad rollout.</li>"
        "<li>Track cost, latency, and security controls from day one.</li>"
        "</ul>"
        "<h2>Sources</h2><ul>"
        + "".join([f"<li><a href=\"{s.link}\">{s.title}</a></li>" for s in sources])
        + "</ul>"
    )
    linkedin_text = (
        f"New post: {title}\n\n"
        "Covered the latest practical AI updates and what they mean for real-world delivery.\n"
        "#AI #LangChain #AzureAI #Cloud #MCP"
    )

    return GeneratedPost(
        title=title,
        slug=slug,
        html_content=html_content,
        excerpt=excerpt,
        linkedin_text=linkedin_text,
        section=primary.section,
        categories=_categories_for_section(primary.section),
    )


def _categories_for_section(section: str) -> List[str]:
    mapping = {
        "ai": ["ai", "cloud"],
        "azure": ["azure", "cloud"],
        "devops": ["devops", "cloud"],
        "terraform": ["terraform", "cloud"],
        "cloud": ["cloud"],
    }
    return mapping.get(section, ["cloud"])


def _is_local_ollama_url(base_url: str) -> bool:
    try:
        parsed = urlparse(base_url)
    except Exception:
        return False
    if parsed.scheme not in {"http", "https"}:
        return False
    return parsed.hostname in {"127.0.0.1", "localhost"} and parsed.port == 11434
