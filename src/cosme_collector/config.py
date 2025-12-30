from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    base_dir: Path
    output_dir: Path
    today: str

    # throttle
    request_sleep_sec: float = 1.3
    retry: int = 3
    timeout: int = 25
    session_pause_every: int = 20
    session_pause_sec: float = 6.0
    image_sleep_sec: float = 0.6

    # headers
    user_agent: str = (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 Chrome/120 Safari/537.36"
    )
    accept_language: str = "ja-JP,ja;q=0.9,en-US;q=0.8,en;q=0.7"


def build_settings(base_dir: Path) -> Settings:
    output_dir = base_dir / "output"
    output_dir.mkdir(exist_ok=True)
    return Settings(
        base_dir=base_dir,
        output_dir=output_dir,
        today=date.today().isoformat(),
    )


def build_paths(settings: Settings, week: int) -> dict[str, Path]:
    """
    cosme_crawler의 결과물은 output/cosme 아래로 모읍니다.
    - CSV: output/cosme/{today}_cosme_rankings_raw.csv
    - Split CSV: output/cosme/{today}_cosme_rankings_csv_split/ -> 제거
    - HTML cache: output/cosme/{today}_html/ -> 제거
    - Images: output/cosme/{today}_images/
    """

    cosme_out_dir = settings.output_dir / "cosme"
    cosme_out_dir.mkdir(parents=True, exist_ok=True)

    # 주차별 CSV 한 파일로 저장
    week_csv = cosme_out_dir / f"week{week}_cosme.csv"

    # 주차별 이미지 폴더
    img_dir = cosme_out_dir / f"week{week}_images"
    img_dir.mkdir(parents=True, exist_ok=True)

    # split_out_dir = cosme_out_dir / f"{settings.today}_cosme_rankings_csv_split"
    # split_out_dir.mkdir(exist_ok=True)

    html_cache_dir = cosme_out_dir / "_html"
    html_cache_dir.mkdir(parents=True, exist_ok=True)

    return {
        "week_csv": week_csv,
        "img_dir": img_dir,
        # "split_out_dir": split_out_dir,
        "html_cache_dir": html_cache_dir,
    }
