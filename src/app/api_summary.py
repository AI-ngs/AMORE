# api_summary.py : 요약 관련 API 라우터
# 서영님 파트

import sqlite3
import re
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
from pathlib import Path

# =========================================================
# [모듈 임포트] 팀원분들의 코드 (크롤러 & 분석기) 활용
# =========================================================
try:
    # GPT 분석기
    from src.review_collector.unified_analyzer import analyze_reviews
    # Amazon 리뷰 로더
    from src.review_collector.unified_pipeline import load_amazon_reviews_by_product
    # [NEW] Cosme 실시간 크롤러
    from src.review_collector.cosme_crawler import crawl_by_id
except ImportError as e:
    print(f"⚠️ 모듈 임포트 경고 (로컬 테스트 시 무시 가능): {e}")
    pass

# =========================
# 1. 경로 및 설정
# =========================
BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "laneige.db"
# Amazon CSV 경로 (unified_pipeline.py와 동일 위치 가정)
AMAZON_CSV_PATH = BASE_DIR / "src" / "review_collector" / "amazon_reviews.CSV"

router = APIRouter(
    prefix="/api/summary",
    tags=["Summary Analysis"]
)

# =========================
# 2. 응답 모델 (프론트엔드 규격)
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
# 3. GPT 응답(줄글) -> JSON 변환 헬퍼
# =========================
def parse_gpt_response(gpt_text: str):
    """
    unified_analyzer.py의 결과(줄글 보고서)에서 키워드와 퍼센트를 추출합니다.
    """
    keywords = ["분석 데이터 없음"]
    sentiment = {"pos": 0, "neu": 0, "neg": 0}
    
    if not gpt_text:
        return keywords, sentiment

    try:
        # 1. 키워드 추출 (예: "1. 키워드: 보습, 향기...")
        # 정규식: '키워드' 뒤에 오는 텍스트 잡기
        keyword_match = re.search(r"키워드.*?[:\n](.*)", gpt_text)
        if keyword_match:
            raw_keywords = keyword_match.group(1).strip()
            # 쉼표로 분리, 특수문자 제거 후 상위 5개
            keywords = [k.strip().replace("-", "").replace(".", "") for k in raw_keywords.split(",")][:5]

        # 2. 감성 비율 추출 (예: "긍정 80%, 중립 10%, 부정 10%")
        # % 앞의 숫자를 찾아서 순서대로 매핑
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
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    try:
        product_name = ""
        current_rank = 0
        rating = 0.0
        total_reviews = 0
        ranking_trend = []
        
        # -------------------------------------------------
        # [Step 1] DB에서 기본 정보 조회 (Amazon / Cosme 공통)
        # -------------------------------------------------
        if source.lower() == 'amazon':
            cursor.execute("SELECT * FROM amazon WHERE productcode = ?", (product_id,))
            rows = cursor.fetchall()
            if not rows: raise HTTPException(status_code=404, detail="Product not found in Amazon DB")
            
            latest = rows[-1]
            product_name = latest['productname']
            current_rank = latest['rank']
            rating = latest['rating']
            
            for i, row in enumerate(rows):
                label = row['crawldate'][:10] if 'crawldate' in row.keys() else f"Week {i+1}"
                ranking_trend.append(RankingPoint(label=label, rank=row['rank']))

        elif source.lower() == 'cosme':
            cursor.execute("SELECT * FROM cosme WHERE product_id = ?", (product_id,))
            rows = cursor.fetchall()
            if not rows: raise HTTPException(status_code=404, detail="Product not found in Cosme DB")
            
            latest = rows[-1]
            # DB에 product_name 컬럼이 있으면 사용, 없으면 브랜드명으로 대체
            product_name = latest['product_name'] if 'product_name' in latest.keys() else f"{latest['brand_name']} Item"
            current_rank = int(latest['global_rank']) if latest['global_rank'] else 0
            rating = latest['rating_score']
            
            for i, row in enumerate(rows):
                label = row['date'] if 'date' in row.keys() else f"Week {i+1}"
                val = int(row['global_rank']) if row['global_rank'] else 0
                ranking_trend.append(RankingPoint(label=label, rank=val))

        # -------------------------------------------------
        # [Step 2] 리뷰 데이터 수집 & 분석 (Source별 분기)
        # -------------------------------------------------
        reviews = []
        
        # Case A: Amazon (CSV 파일 로드)
        if source.lower() == 'amazon':
            target_key = product_name.lower().replace(" ", "")
            # 팀원 코드를 활용해 CSV에서 로드
            reviews = load_amazon_reviews_by_product(str(AMAZON_CSV_PATH), target_key)
            
            # 정확한 매칭이 없으면 'Laneige' 키워드로 재검색 (Fallback)
            if not reviews and "laneige" in product_name.lower():
                reviews = load_amazon_reviews_by_product(str(AMAZON_CSV_PATH), "laneige")

        # Case B: Cosme (실시간 크롤링)
        elif source.lower() == 'cosme':
            print(f"🚀 [Cosme] ID {product_id} 실시간 크롤링 시작...")
            try:
                # 속도를 위해 max_pages=1 (약 20개 리뷰)로 제한
                reviews = crawl_by_id(product_id, max_pages=1)
                print(f"✅ [Cosme] 리뷰 {len(reviews)}건 수집 완료")
            except Exception as e:
                print(f"❌ [Cosme] 크롤링 실패: {e}")
                reviews = []

        # -------------------------------------------------
        # [Step 3] GPT 분석 실행
        # -------------------------------------------------
        keywords = ["리뷰 부족"]
        sentiment_dict = {"pos": 0, "neu": 0, "neg": 0}

        if reviews:
            # 분석 실행 (Unified Analyzer 활용)
            gpt_report = analyze_reviews(product_name, reviews, source)
            
            # 결과 파싱
            keywords, sentiment_dict = parse_gpt_response(gpt_report)
            
            # 실제 리뷰 개수 업데이트
            total_reviews = len(reviews)
        else:
            # 리뷰가 없을 경우 DB에 있는 review_count 사용 (있다면)
            if source.lower() == 'amazon':
                total_reviews = latest['reviewcount'] if 'reviewcount' in latest.keys() else 0
            elif source.lower() == 'cosme':
                total_reviews = latest['review_count'] if 'review_count' in latest.keys() else 0

        # -------------------------------------------------
        # [Step 4] 최종 반환
        # -------------------------------------------------
        return ProductSummaryResponse(
            product_id=product_id,
            product_name=product_name,
            source=source,
            basic_analysis=BasicAnalysis(
                current_ranking=current_rank,
                rank_change=0, # 과거 데이터가 충분하면 계산 가능
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