from __future__ import annotations

import time
import requests
from bs4 import BeautifulSoup

from src.cosme_collector.config import Settings


def build_session(settings):
    s = requests.Session()
    s.headers.update({
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "ja,en-US;q=0.9,en;q=0.8,ko;q=0.7",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    })
    return s


def _looks_blocked_or_wrong(html: str, requested_url: str = "") -> bool:
    if not html:
        return True

    soup = BeautifulSoup(html, "html.parser")
    title = (soup.title.get_text(" ", strip=True) if soup.title else "") or ""

    # 확실한 로그인/가입 페이지 타이틀만 강하게 차단
    if "ログイン／メンバー登録" in title:
        return True
    if "共通ID登録" in title:
        return True

    # 블로그 쪽만 canonical 체크 (제품 랭킹에는 적용 X)
    if "/beautist" in requested_url:
        canon = soup.select_one('link[rel="canonical"]')
        canonical = (canon.get("href") if canon else "") or ""
        if canonical.rstrip("/") == "https://www.cosme.net/beautist":
            return True

    # “문구 기반 차단 판단”은 블로그에서만 적용
    if "/beautist" in requested_url:
        txt = soup.get_text("\n", strip=True)
        if "会員登録(無料)" in txt and "ログイン" in txt and "ブログ TOP" not in txt:
            return True

    return False


def fetch_html_safe(session: requests.Session, settings: Settings, url: str) -> str:
    last_err = None
    for i in range(settings.retry):
        try:
            r = session.get(url, timeout=settings.timeout, allow_redirects=True)
            r.raise_for_status()
            html = r.text or ""

            if _looks_blocked_or_wrong(html, requested_url=url):
                raise RuntimeError(f"BLOCKED/WRONG PAGE: {url}  final={r.url}")

            return html

        except Exception as e:
            last_err = e
            time.sleep(1.0 + i)

    raise RuntimeError(f"FETCH FAILED: {url} :: {last_err}")
