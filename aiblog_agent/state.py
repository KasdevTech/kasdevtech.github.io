from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Optional

DB_PATH = Path(".aiblog_state.sqlite3")


def _state_file_path(custom_path: str = "") -> Optional[Path]:
    if not custom_path.strip():
        return None
    return Path(custom_path).expanduser().resolve()


def _read_state_file(path: Path) -> set[str]:
    if not path.exists():
        return set()
    lines = [line.strip() for line in path.read_text(encoding="utf-8").splitlines()]
    return {line for line in lines if line}


def _write_state_file(path: Path, urls: set[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(sorted(urls)) + "\n", encoding="utf-8")


def init_db(custom_path: str = "") -> None:
    if _state_file_path(custom_path) is not None:
        return
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS published_sources (
                source_url TEXT PRIMARY KEY,
                wordpress_post_url TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()


def was_source_published(source_url: str, custom_path: str = "") -> bool:
    file_path = _state_file_path(custom_path)
    if file_path is not None:
        return source_url in _read_state_file(file_path)

    with sqlite3.connect(DB_PATH) as conn:
        row = conn.execute(
            "SELECT 1 FROM published_sources WHERE source_url = ? LIMIT 1",
            (source_url,),
        ).fetchone()
    return row is not None


def mark_source_published(source_url: str, wordpress_post_url: str, custom_path: str = "") -> None:
    file_path = _state_file_path(custom_path)
    if file_path is not None:
        urls = _read_state_file(file_path)
        urls.add(source_url)
        _write_state_file(file_path, urls)
        return

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            INSERT OR REPLACE INTO published_sources(source_url, wordpress_post_url)
            VALUES (?, ?)
            """,
            (source_url, wordpress_post_url),
        )
        conn.commit()
