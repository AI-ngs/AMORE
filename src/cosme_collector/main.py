from __future__ import annotations

from pathlib import Path
import argparse

from src.cosme_collector.config import build_settings, build_paths
from src.cosme_collector.jobs import build_jobs
from src.cosme_collector.http_client import build_session, fetch_html_safe
from src.cosme_collector.pipeline import run_all, quality_checks


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true")
    parser.add_argument("--week", type=int, required=True)
    args = parser.parse_args()

    base_dir = Path(__file__).resolve().parents[1]

    settings = build_settings(base_dir)
    paths = build_paths(settings, week=args.week)
    jobs = build_jobs(test_mode=args.test)

    session = build_session(settings)
    fetch_fn = lambda url: fetch_html_safe(session, settings, url)

    df = run_all(
        session=session,
        settings=settings,
        jobs=jobs,
        html_cache_dir=paths["html_cache_dir"],
        img_dir=paths["img_dir"],
        fetch_html_fn=fetch_fn,
        download_images=True,
    )

    for job in jobs:
        quality_checks(df, job)

    import shutil

    # 주차 파일 1개만 저장
    df.to_csv(paths["week_csv"], index=False, encoding="utf-8-sig")
    print(f"[OK] saved: {paths['week_csv']}")

    # HTML cache: run_all 인터페이스 맞추기 위해 임시 폴더만 생성 후 실행 종료 시 삭제
    shutil.rmtree(paths["html_cache_dir"], ignore_errors=True)
    print("[CLEANUP] html cache removed")

if __name__ == "__main__":
    main()
