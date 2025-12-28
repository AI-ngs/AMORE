# src/database/cosme_table.py
# amazon 테이블에 CSV 데이터를 적재하는 스크립트
# 기존에 있던 amazon 테이블을 삭제하고, output/amazon 폴더의 모든 CSV 파일을 읽어와서 amazon 테이블에 적재함

import sqlite3
from pathlib import Path
import pandas as pd


# =========================
# 경로 설정
# =========================
BASE_DIR = Path(__file__).resolve().parents[2]  # AMORE
OUTPUT_DIR = BASE_DIR / "output" / "amazon"
DB_PATH = BASE_DIR / "laneige.db"


# =========================
# DB 저장 로직
# =========================
def save_csvs_to_sqlite():
    print(f"[INFO] DB 경로: {DB_PATH}")
    print(f"[INFO] CSV 폴더: {OUTPUT_DIR}")

    csv_files = list(OUTPUT_DIR.glob("*.csv"))
    if not csv_files:
        print("[WARN] CSV 파일이 없습니다.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 기존 테이블 삭제
    print("[INFO] 기존 amazon 테이블 삭제")
    cursor.execute("DROP TABLE IF EXISTS amazon")
    conn.commit()

    # CSV → DB
    for csv_file in csv_files:
        print(f"[LOAD] {csv_file.name}")
        df = pd.read_csv(csv_file)

        df.to_sql(
            name="amazon",
            con=conn,
            if_exists="append",
            index=False
        )

    conn.close()
    print("[DONE] cosme 테이블 재생성 및 CSV 적재 완료")


# =========================
# 실행
# =========================
if __name__ == "__main__":
    save_csvs_to_sqlite()
