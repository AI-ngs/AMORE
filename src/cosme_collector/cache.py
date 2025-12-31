from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import quote


def safe_filename(s: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9_\-]+", "_", s)
    return s[:180]


def cache_path_for(html_cache_dir: Path, job: dict, url: str) -> Path:
    key = f'{job["category_id"]}__{job["ranking_type"]}__{quote(url, safe="")}'
    return html_cache_dir / (safe_filename(key) + ".html")


def load_or_save_html(
    html_cache_dir: Path,
    job: dict,
    url: str,
    fetch_fn,
    force_refresh: bool = False,
) -> str:
    path = cache_path_for(html_cache_dir, job, url)
    if path.exists() and not force_refresh:
        html = path.read_text(encoding="utf-8", errors="ignore")

        if len(html) > 5000 and "</html>" in html.lower():
            return html

    html = fetch_fn(url)
    path.write_text(html, encoding="utf-8", errors="ignore")
    return html
