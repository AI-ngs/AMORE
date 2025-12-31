from __future__ import annotations

import re
import time
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse, parse_qs

import pandas as pd
import requests

from src.cosme_collector.config import Settings
from src.cosme_collector.image_downloader import download_image_safe
from src.cosme_collector.parsers import parse_grouped_keyword_ranking, parse_page_items_ordered
from src.cosme_collector.util import rule_split


@dataclass
class Row:
    date: str
    collected_at: str
    source: str
    market: str
    category_id: str
    category_name: str
    ranking_type: str
    ranking_url: str

    global_rank: Optional[int]
    page_rank: Optional[int]

    group_type: Optional[str]
    group_value: Optional[str]
    group_rank: Optional[int]

    product_id: Optional[str]
    product_name: Optional[str]
    brand_name: Optional[str]
    product_url: Optional[str]
    image_url: Optional[str]      # 원본 URL
    image_path: Optional[str]     # 로컬 저장 경로(옵션)

    rating_score: Optional[float]
    review_count: Optional[int]
    price_text: Optional[str]
    rank_change_text: Optional[str]
    brand_url: Optional[str]

_LANEIGE_PAT = re.compile(r"(laneige|라네즈|ラネージュ)", re.IGNORECASE)

def is_laneige(brand_name: Optional[str]) -> bool:
    """브랜드명이 라네즈(LANEIGE)인지 판별."""
    if not brand_name:
        return False
    return bool(_LANEIGE_PAT.search(brand_name.strip()))

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def append_csv(path: Path, df: pd.DataFrame):
    if path.exists():
        df.to_csv(path, mode="a", header=False, index=False, encoding="utf-8-sig")
    else:
        df.to_csv(path, mode="w", header=True, index=False, encoding="utf-8-sig")


def split_and_save(df: pd.DataFrame, split_out_dir: Path):
    for rtype, sub in df.groupby("ranking_type"):
        safe = re.sub(r"[^a-zA-Z0-9_\-]+", "_", rtype)
        out = split_out_dir / f"{safe}.csv"
        sub.to_csv(out, index=False, encoding="utf-8-sig")


def quality_checks(df: pd.DataFrame, job: dict):
    """
    QC: job 설정(target_n)에 맞게 랭킹 개수 검증
    """

    # rank 컬럼 없으면 QC 패스
    if "global_rank" not in df.columns:
        return

    kind = job.get("kind")
    ranking_type = job.get("ranking_type")
    category_id = job.get("category_id")

    # -------------------------
    # topN_pages (Top100 / 테스트 Top10)
    # -------------------------
    if kind == "topN_pages":
        target_n = int(job.get("target_n", 0))
        if target_n <= 0:
            return

        sub = df[df["ranking_type"] == ranking_type]
        ranks = set(sub["global_rank"].dropna().astype(int))
        expected = set(range(1, target_n + 1))
        missing = sorted(expected - ranks)

        if missing:
            raise RuntimeError(
                f"[QC] {ranking_type} 누락: {missing[:20]} ... (총 {len(missing)}개)"
            )

    # -------------------------
    # topN_query_pages (Top50)
    # -------------------------
    if kind == "topN_query_pages":
        target_n = int(job.get("target_n", 0))
        if target_n <= 0:
            return

        sub = df[
            (df["category_id"] == category_id)
            & (df["ranking_type"] == ranking_type)
        ]
        ranks = set(sub["global_rank"].dropna().astype(int))
        expected = set(range(1, target_n + 1))
        missing = sorted(expected - ranks)

        if missing:
            raise RuntimeError(
                f"[QC] category {category_id} {ranking_type} 누락: {missing}"
            )

    # -------------------------
    # rise (Top10)
    # -------------------------
    if kind == "rise":
        sub = df[
            (df["category_id"] == category_id)
            & (df["ranking_type"] == ranking_type)
        ]
        if len(sub) > 0:
            ranks = set(sub["global_rank"].dropna().astype(int))
            expected = set(range(1, 11))
            missing = sorted(expected - ranks)

            if missing:
                raise RuntimeError(
                    f"[QC] category {category_id} {ranking_type} 누락: {missing}"
                )


def _calc_offset(job: dict, url: str) -> tuple[int, int]:
    """
    (offset, page_no) 반환
    - products_top100 : urls index 기반
    - topN_query_pages : ?page=2.. 파싱
    - rise : offset=0
    """
    kind = job["kind"]
    if job["ranking_type"] == "products_top100":
        idx_in_list = job["urls"].index(url)  # 0..9
        return idx_in_list * job.get("page_size", 10), idx_in_list + 1

    if kind == "topN_query_pages":
        page_param = job.get("page_param", "page")
        q = parse_qs(urlparse(url).query)
        page_no = int((q.get(page_param, ["1"])[0] or "1"))
        offset = (page_no - 1) * job.get("page_size", 10)
        return offset, page_no

    # rise / 기타
    return 0, 1


def run_all(
    session: requests.Session,
    settings: Settings,
    jobs: list[dict],
    html_cache_dir: Path,
    img_dir: Path,
    fetch_html_fn,              # lambda url: fetch_html_safe(...)
    download_images: bool = True,
) -> pd.DataFrame:
    all_rows: list[Row] = []
    req_count = 0

    total_pages = sum(len(job["urls"]) for job in jobs)
    done_pages = 0

    for job in jobs:
        print(f"[JOB] {job['category_id']} / {job['ranking_type']}", flush=True)
        for url in job["urls"]:
            done_pages += 1
            pct = done_pages / total_pages * 100
            print(
                f"[PROGRESS] pages {done_pages}/{total_pages} ({pct:.1f}%)",
                flush=True,
            )
            print(f"  [GET] {url}", flush=True)

            req_count += 1
            if req_count % settings.session_pause_every == 0:
                print(f"  [PAUSE] {settings.session_pause_sec}s (every {settings.session_pause_every} req)", flush=True)
                time.sleep(settings.session_pause_sec)

            # html 추출 막기
            # html = load_or_save_html(
            #     html_cache_dir=html_cache_dir,
            #     job=job,
            #     url=url,
            #     fetch_fn=fetch_html_fn,
            #     force_refresh=False,
            # )
            html = fetch_html_fn(url)
            time.sleep(settings.request_sleep_sec)

            kind = job["kind"]

            if kind in ("topN_query_pages", "topN_pages", "rise"):
                limit = job.get("page_size", 10)
                items = parse_page_items_ordered(html, limit=limit)

                offset, _ = _calc_offset(job, url)

                for i, item in enumerate(items, start=1):
                    global_rank = offset + i

                    image_path = None
                    if download_images and is_laneige(item.get("brand_name") or item.get("product_name")) and item.get("image_url") and item.get("product_id"):
                        stem = f'{job["category_id"]}__{job["ranking_type"]}__{global_rank}__{item["product_id"]}'
                        p = download_image_safe(
                            session=session,
                            url=item["image_url"],
                            out_dir=img_dir,
                            filename_stem=stem,
                            retry=settings.retry,
                            timeout=settings.timeout,
                            sleep_sec=settings.image_sleep_sec,
                        )
                        if p:
                            try:
                                image_path = str(p.relative_to(settings.base_dir))
                            except ValueError:
                                # 실패하면 fallback
                                image_path = str(p)

                    all_rows.append(
                        Row(
                            date=settings.today,
                            collected_at=now_iso(),
                            source=job["source"],
                            market=job["market"],
                            category_id=job["category_id"],
                            category_name=job["category_name"],
                            ranking_type=job["ranking_type"],
                            ranking_url=url,
                            global_rank=global_rank,
                            page_rank=i,
                            group_type=None,
                            group_value=None,
                            group_rank=None,
                            product_id=item.get("product_id"),
                            product_name=rule_split(
                                item.get("product_name"),
                                item.get("brand_name")
                            ),
                            brand_name=item.get("brand_name"),
                            product_url=item.get("product_url"),
                            image_url=item.get("image_url"),
                            image_path=image_path,
                            rating_score=item.get("rating_score"),
                            review_count=item.get("review_count"),
                            price_text=item.get("price_text"),
                            rank_change_text=item.get("rank_change_text"),
                            brand_url=item.get("brand_url"),
                        )
                    )

            elif kind == "grouped":
                group_type = job["group_type"]
                max_each = 2 if group_type == "cross" else 3

                rows = parse_grouped_keyword_ranking(html, max_each_group=max_each)
                for r in rows:
                    image_path = None

                    if (
                        download_images
                        and is_laneige(r.get("brand_name") or r.get("product_name"))
                        and r.get("image_url")
                        and r.get("product_id")
                    ):
                        stem = f'{job["category_id"]}__{job["ranking_type"]}__{group_type}__{r.get("group_value")}__{r.get("group_rank")}__{r["product_id"]}'
                        stem = re.sub(r"[^a-zA-Z0-9_\-]+", "_", stem)[:180]

                        p = download_image_safe(
                            session=session,
                            url=r["image_url"],
                            out_dir=img_dir,
                            filename_stem=stem,
                            retry=settings.retry,
                            timeout=settings.timeout,
                            sleep_sec=settings.image_sleep_sec,
                        )

                        if p:
                            try:
                                image_path = str(p.relative_to(settings.base_dir))
                            except ValueError:
                                image_path = str(p)

                    all_rows.append(
                        Row(
                            date=settings.today,
                            collected_at=now_iso(),
                            source=job["source"],
                            market=job["market"],
                            category_id=job["category_id"],
                            category_name=job["category_name"],
                            ranking_type=job["ranking_type"],
                            ranking_url=url,
                            global_rank=None,
                            page_rank=None,
                            group_type=group_type,
                            group_value=r.get("group_value"),
                            group_rank=r.get("group_rank"),
                            product_id=r.get("product_id"),
                            product_name=rule_split(
                                r.get("product_name"),
                                r.get("brand_name")
                            ),
                            brand_name=r.get("brand_name"),
                            product_url=r.get("product_url"),
                            image_url=r.get("image_url"),
                            image_path=image_path,
                            rating_score=r.get("rating_score"),
                            review_count=r.get("review_count"),
                            price_text=r.get("price_text"),
                            rank_change_text=r.get("rank_change_text"),
                            brand_url=r.get("brand_url"),
                        )
                    )
            else:
                raise ValueError(f"Unknown kind: {kind}")

    df = pd.DataFrame([asdict(r) for r in all_rows])

    if not df.empty:
        df = df.drop_duplicates(
            subset=["date", "ranking_type", "ranking_url", "product_id"],
            keep="last",
        )

    return df
