from __future__ import annotations
import os
import re
import pandas as pd
from typing import List

FILES = [
    "output/cosme/week2/week2_cosme.csv",
    "output/cosme/week3/week3_cosme.csv",
]

OUT_DIR = "output/cosme"
os.makedirs(OUT_DIR, exist_ok=True)

OUT_WEEK2_TO_WEEK3 = os.path.join(OUT_DIR, "week2toweek3_cosme_rank.csv")

KEY_COLS = ["category_id", "ranking_type", "group_type", "group_value", "product_id"]

def normalize_name(s: str) -> str:
    if pd.isna(s):
        return ""
    s = str(s)
    s = s.replace("（", "(").replace("）", ")")
    s = s.replace("\u3000", " ")
    s = re.sub(r"\s+", " ", s).strip()
    s = re.sub(r"\b(NEW|限定|人気|再入荷)\b", "", s, flags=re.IGNORECASE)
    s = re.sub(r"\s+", " ", s).strip()
    return s

def week_from_path(fp: str) -> str:
    m = re.search(r"(week\d+)", fp)
    return m.group(1) if m else os.path.basename(fp)

def load_and_prepare(files: List[str]) -> pd.DataFrame:
    dfs = []
    for fp in files:
        df = pd.read_csv(fp)
        df["__source_file"] = os.path.basename(fp)

        week = week_from_path(fp)
        df["snapshot"] = week  # 비교용 라벨 추가

        # 원본 date는 유지 (없으면 빈값으로)
        if "date" not in df.columns:
            df["date"] = ""
        df["date"] = df["date"].astype(str)

        # 결측 보정 (없으면 만들어줌)
        if "group_type" not in df.columns:
            df["group_type"] = ""
        if "group_value" not in df.columns:
            df["group_value"] = ""
        if "brand_name" not in df.columns:
            df["brand_name"] = ""
        if "product_name" not in df.columns:
            df["product_name"] = ""

        dfs.append(df)

    df = pd.concat(dfs, ignore_index=True)

    # 상품명 정규화
    df["product_name_raw"] = df["product_name"].astype(str)
    df["product_name_norm"] = df["product_name_raw"].apply(normalize_name)

    # rank_value
    if "group_rank" not in df.columns:
        df["group_rank"] = pd.NA
    if "global_rank" not in df.columns:
        df["global_rank"] = pd.NA

    df["rank_value"] = df["group_rank"].where(df["group_rank"].notna(), df["global_rank"])
    df["rank_value"] = pd.to_numeric(df["rank_value"], errors="coerce")

    # snapshot별 중복 제거
    df = df.sort_values(["snapshot", "rank_value"]).drop_duplicates(
        subset=["snapshot"] + KEY_COLS,
        keep="first"
    )
    return df

def between_dates_table(panel: pd.DataFrame) -> pd.DataFrame:
    snaps = sorted(
        panel["snapshot"].unique(),
        key=lambda x: int(re.search(r"\d+", x).group()) if re.search(r"\d+", x) else 0
    )
    rows = []

    for i in range(1, len(snaps)):
        prev_d, cur_d = snaps[i - 1], snaps[i]
        prev = panel[panel["snapshot"] == prev_d].copy()
        cur  = panel[panel["snapshot"] == cur_d].copy()

        prev_small = prev[KEY_COLS + ["rank_value", "product_name", "brand_name", "date"]].rename(
            columns={
                "rank_value": "rank_value_prev",
                "product_name": "product_name_prev",
                "brand_name": "brand_name_prev",
                "date": "date_prev",
            }
        )
        cur_small = cur[KEY_COLS + ["rank_value", "product_name", "brand_name", "date"]].rename(
            columns={
                "rank_value": "rank_value_cur",
                "product_name": "product_name_cur",
                "brand_name": "brand_name_cur",
                "date": "date_cur",
            }
        )

        merged = prev_small.merge(cur_small, on=KEY_COLS, how="outer", indicator=True)

        def status(row):
            if row["_merge"] == "left_only":
                return "dropped"
            if row["_merge"] == "right_only":
                return "new"
            if row["rank_value_cur"] == row["rank_value_prev"]:
                return "same"
            return "up" if row["rank_value_cur"] < row["rank_value_prev"] else "down"

        merged["status"] = merged.apply(status, axis=1)
        merged["rank_value_diff"] = merged["rank_value_cur"] - merged["rank_value_prev"]
        merged["rank_value_moved_by"] = merged["rank_value_diff"].abs()

        merged["from_snapshot"] = prev_d
        merged["to_snapshot"] = cur_d

        rows.append(merged)

    return pd.concat(rows, ignore_index=True)

if __name__ == "__main__":
    base = load_and_prepare(FILES)
    between = between_dates_table(base)

    out = between[(between["from_snapshot"] == "week2") & (between["to_snapshot"] == "week3")].copy()
    out.to_csv(OUT_WEEK2_TO_WEEK3, index=False, encoding="utf-8-sig")
    print("saved:", OUT_WEEK2_TO_WEEK3)
