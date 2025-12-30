# src/database/test_table.py
# 데이터베이스의 테이블과 일부 데이터가 잘 들어갔는지 확인하는 테스트용 스크립트

import sqlite3
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "laneige.db"

conn = sqlite3.connect(DB_PATH)

# 테이블 목록
tables = conn.execute(
    "SELECT name FROM sqlite_master WHERE type='table';"
).fetchall()

print("📌 테이블 목록:")
for t in tables:
    print("-", t[0])

# 데이터 확인
df = pd.read_sql("SELECT * FROM amazon LIMIT 5", conn)
print(df)

df_count = pd.read_sql(
    "SELECT COUNT(*) as cnt FROM amazon",
    conn
)
print(df_count)


conn.close()
