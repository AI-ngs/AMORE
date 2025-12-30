# api_summary.py : 요약 관련 API 라우터
# 서영님 파트

import sqlite3
import re
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
from pathlib import Path

# =========================================================
# [모듈 임포트] 크롤러 & 분석기
# =========================================================
try:
    from src.review_collector.unified_analyzer import analyze_reviews
    from src.review_collector.unified_pipeline import load_amazon_reviews_by_product
    from src.review_collector.cosme_crawler import crawl_by_id
except ImportError as e:
    print(f"⚠️ 모듈 임포트 경고: {e}")
    pass

# =========================
# 1. 경로 및 설정
# =========================
BASE_DIR = Path(__file__).resolve().parents[2]

# 모든 데이터는 laneige.db에 통합되어 있음
DB_PATH = BASE_DIR / "laneige.db"

# Amazon CSV 경로
AMAZON_CSV_PATH = BASE_DIR / "src" / "review_collector" / "amazon_reviews.CSV"

router = APIRouter(
    prefix="/api/summary",
    tags=["Summary Analysis"]
)

# =========================
# 2. 응답 모델
# =========================
class BasicAnalysis(BaseModel):
    current_ranking: Optional[int]
    rank_change: Optional[int]
    total_reviews: int
    rating: float

class RankingPoint(BaseModel):
    label: str
    rank: Optional[int]

class SentimentData(BaseModel):
    positive: int
    neutral: int
    negative: int

class ProductSummaryResponse(BaseModel):
    product_id: str
    product_name: str
    source: str
    basic_analysis: BasicAnalysis
    ranking_trend: List[RankingPoint]
    keywords: List[str]
    sentiment: SentimentData

# =========================
# 3. 헬퍼 함수
# =========================
def parse_gpt_response(gpt_text: str):
    """ GPT 결과(줄글)를 파싱하여 키워드 리스트와 감성 수치로 변환 """
    keywords = ["분석 중..."]
    sentiment = {"pos": 0, "neu": 0, "neg": 0}
    
    if not gpt_text:
        return keywords, sentiment

    try:
        # 키워드 추출
        keyword_match = re.search(r"키워드.*?[:\n](.*)", gpt_text)
        if keyword_match:
            raw_keywords = keyword_match.group(1).strip()
            keywords = [k.strip().replace("-", "").replace(".", "") for k in raw_keywords.split(",")][:5]

        # 감성 비율 추출
        numbers = re.findall(r"(\d+)%", gpt_text)
        if len(numbers) >= 3:
            sentiment["pos"] = int(numbers[0])
            sentiment["neu"] = int(numbers[1])
            sentiment["neg"] = int(numbers[2])
    except Exception as e:
        print(f"GPT 파싱 에러: {e}")
    
    return keywords, sentiment

# =========================
# 4. API 엔드포인트
# =========================
@router.get("/{product_id}", response_model=ProductSummaryResponse)
async def get_product_summary(
    product_id: str, 
    source: str = Query(..., description="amazon 또는 cosme")
):
    if not DB_PATH.exists():
         raise HTTPException(status_code=500, detail="Database file (laneige.db) not found.")

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    try:
        product_name = ""
        current_rank = 0
        rating = 0.0
        total_reviews = 0
        ranking_trend = []
        rank_change = 0
        
        # -------------------------------------------------
        # [Step 1] DB 조회 (테이블 분기)
        # -------------------------------------------------
        if source.lower() == 'amazon':
            # amazon 테이블 조회
            cursor.execute("SELECT * FROM amazon WHERE productcode = ? ORDER BY crawldate ASC", (product_id,))
            rows = cursor.fetchall()
            
            if not rows: raise HTTPException(status_code=404, detail="Product not found in Amazon DB")
            
            latest = rows[-1]
            product_name = latest['productname']
            current_rank = latest['rank']
            rating = latest['rating']
            
            if len(rows) >= 2:
                prev_rank = rows[-2]['rank']
                rank_change = prev_rank - current_rank
            
            for row in rows:
                label = row['crawldate'][:10] if 'crawldate' in row.keys() else "Date"
                ranking_trend.append(RankingPoint(label=label, rank=row['rank']))

        elif source.lower() == 'cosme':
            # cosme 테이블 조회 (laneige.db 안에 있음)
            cursor.execute("SELECT * FROM cosme WHERE product_id = ? ORDER BY date ASC", (product_id,))
            rows = cursor.fetchall()
            
            if not rows: raise HTTPException(status_code=404, detail="Product not found in Cosme DB")
            
            latest = rows[-1]
            product_name = latest['product_name'] if 'product_name' in latest.keys() else f"{latest['brand_name']} Item"
            current_rank = int(latest['global_rank']) if latest['global_rank'] else 0
            rating = latest['rating_score']

            if len(rows) >= 2:
                prev_val = int(rows[-2]['global_rank']) if rows[-2]['global_rank'] else 0
                if prev_val > 0 and current_rank > 0:
                    rank_change = prev_val - current_rank
            
            for row in rows:
                label = row['date'] if 'date' in row.keys() else "Date"
                val = int(row['global_rank']) if row['global_rank'] else 0
                ranking_trend.append(RankingPoint(label=label, rank=val))

        # -------------------------------------------------
        # [Step 2] 리뷰 분석 (Live Crawling or CSV)
        # -------------------------------------------------
        reviews = []
        
        # Amazon: CSV 파일 사용
        if source.lower() == 'amazon':
            target_key = product_name.lower().replace(" ", "")
            reviews = load_amazon_reviews_by_product(str(AMAZON_CSV_PATH), target_key)
            if not reviews and "laneige" in product_name.lower():
                 pass # Fallback 로직 필요시 추가

        # Cosme: 실시간 크롤링 (속도 이슈로 1페이지 제한)
        elif source.lower() == 'cosme':
            try:
                reviews = crawl_by_id(product_id, max_pages=1)
            except Exception:
                reviews = []

        # -------------------------------------------------
        # [Step 3] GPT 분석 및 결과 반환
        # -------------------------------------------------
        keywords = ["데이터 부족"]
        sentiment_dict = {"pos": 0, "neu": 0, "neg": 0}

        if reviews:
            gpt_report = analyze_reviews(product_name, reviews, source)
            keywords, sentiment_dict = parse_gpt_response(gpt_report)
            total_reviews = len(reviews)
        else:
            if source.lower() == 'amazon':
                total_reviews = latest['reviewcount'] if 'reviewcount' in latest.keys() else 0
            elif source.lower() == 'cosme':
                total_reviews = latest['review_count'] if 'review_count' in latest.keys() else 0

        return ProductSummaryResponse(
            product_id=product_id,
            product_name=product_name,
            source=source,
            basic_analysis=BasicAnalysis(
                current_ranking=current_rank,
                rank_change=rank_change,
                total_reviews=total_reviews,
                rating=rating
            ),
            ranking_trend=ranking_trend,
            keywords=keywords,
            sentiment=SentimentData(
                positive=sentiment_dict['pos'],
                neutral=sentiment_dict['neu'],
                negative=sentiment_dict['neg']
            )
        )

    finally:
        conn.close()