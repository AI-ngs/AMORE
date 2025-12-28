import sqlite3
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "cosme.db"

conn = sqlite3.connect(DB_PATH)

# 테이블 목록
tables = conn.execute(
    "SELECT name FROM sqlite_master WHERE type='table';"
).fetchall()

print("📌 테이블 목록:")
for t in tables:
    print("-", t[0])

# 데이터 확인
df = pd.read_sql("SELECT * FROM cosme LIMIT 5", conn)
print(df)

conn.close()
