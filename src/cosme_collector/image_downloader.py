from __future__ import annotations

import hashlib
import time
from pathlib import Path
from urllib.parse import urlparse

import requests


def _safe_ext(url: str) -> str:
    try:
        ext = Path(urlparse(url).path).suffix.lower()
        if ext in [".jpg", ".jpeg", ".png", ".gif", ".webp"]:
            return ext
    except Exception:
        pass
    return ".jpg"


def download_image_safe(
    session: requests.Session,
    url: str,
    out_dir: Path,
    filename_stem: str | None = None,
    filename_prefix: str | None = None,  # ✅ 호환용
    retry: int = 3,
    timeout: int = 25,
    sleep_sec: float = 0.0,
) -> Path | None:
    """
    실패해도 None 반환
    """
    if not url:
        return None

    out_dir.mkdir(parents=True, exist_ok=True)

    stem = filename_stem or filename_prefix or ""
    h = hashlib.sha1(url.encode("utf-8")).hexdigest()[:12]
    ext = _safe_ext(url)
    fname = f"{stem}_{h}{ext}" if stem else f"{h}{ext}"
    out_path = out_dir / fname

    if out_path.exists() and out_path.stat().st_size > 0:
        return out_path

    last = None
    for i in range(retry):
        try:
            r = session.get(url, timeout=timeout)
            r.raise_for_status()
            out_path.write_bytes(r.content)
            if sleep_sec:
                time.sleep(sleep_sec)
            return out_path
        except Exception as e:
            last = e
            time.sleep(0.8 + i)

    return None
