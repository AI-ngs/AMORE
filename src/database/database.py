import sqlite3
from pathlib import Path
import pandas as pd


# =========================
# 경로 설정
# =========================
BASE_DIR = Path(__file__).resolve().parents[2]  # AMORE
OUTPUT_DIR = BASE_DIR / "output"
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

    for csv_file in csv_files:
        print(f"[LOAD] {csv_file.name}")

        df = pd.read_csv(csv_file)

        # 핵심: 하나의 테이블에 계속 데이터 append
        df.to_sql(
            name="cosme",
            con=conn,
            if_exists="append",   # ← 누적
            index=False
        )

    conn.close()
    print("[DONE] 모든 CSV 저장 완료")


# =========================
# 실행 진입점
# =========================
if __name__ == "__main__":
    save_csvs_to_sqlite()
