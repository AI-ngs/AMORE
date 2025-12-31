from __future__ import annotations

import re
from pathlib import Path
from typing import Union


# -------------------------
# 상품명 split
# -------------------------
def rule_split(product_name, brand_name=None):
    if not product_name:
        return product_name

    s = str(product_name).strip()

    if brand_name:
        b = str(brand_name).strip()
        if b and s.startswith(b):
            parts = re.split(r"\s*[\/／]\s*", s, maxsplit=1)
            return parts[1].strip() if len(parts) == 2 else s
        return s

    parts = re.split(r"\s*[\/／]\s*", s, maxsplit=1)
    return parts[1].strip() if len(parts) == 2 else s


# -------------------------
# output 디렉토리 생성
# -------------------------
def build_output_dirs(
    output_root: Union[str, Path],
    job_name: str,
    date_str: str,
) -> dict[str, Path]:
    """
    output/
      job_name/
        YYYY-MM-DD/
          html/
          images/
          csv/
    """
    base = Path(output_root) / job_name / date_str
    html_dir = base / "html"
    img_dir = base / "images"
    csv_dir = base / "csv"

    html_dir.mkdir(parents=True, exist_ok=True)
    img_dir.mkdir(parents=True, exist_ok=True)
    csv_dir.mkdir(parents=True, exist_ok=True)

    return {
        "base": base,
        "html": html_dir,
        "images": img_dir,
        "csv": csv_dir,
    }
