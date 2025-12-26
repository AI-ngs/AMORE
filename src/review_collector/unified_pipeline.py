import csv
import os
from collections import defaultdict
from datetime import datetime, timedelta

import cosme_crawler
from unified_analyzer import analyze_reviews


# =========================
# 날짜 파싱 (Amazon용)
# =========================
def parse_amazon_date(date_str):
    """
    지원 형식:
    - 19-Dec-25
    - 2024-12-19
    """
    for fmt in ("%d-%b-%y", "%Y-%m-%d"):
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            pass
    return None


# =========================
# Amazon CSV → 제품별 + 기간 필터
# =========================
def load_amazon_reviews_by_product(csv_path, days=None):
    product_reviews = defaultdict(list)

    if days is not None:
        cutoff_date = datetime.today() - timedelta(days=days)
    else:
        cutoff_date = None

    with open(csv_path, mode="r", encoding="utf-8-sig", errors="ignore") as f:
        reader = csv.DictReader(f)
        for row in reader:
            product = row.get("product_name", "").strip()
            review = row.get("review_text", "").strip()
            date_str = row.get("review_date", "").strip()

            if not product or not review or not date_str:
                continue

            review_date = parse_amazon_date(date_str)
            if not review_date:
                continue

            if cutoff_date and review_date < cutoff_date:
                continue

            product_reviews[product].append(review)

    return product_reviews


def run_pipeline():
    print("\n[리뷰 분석 시스템]")
    print("1. Amazon (US)")
    print("2. @COSME (JP)")
    site_choice = input("사이트를 선택하세요 (1/2): ").strip()

    print("\n[기간 설정]")
    print("1. 7일 | 2. 30일 | 3. 90일 | 4. 180일 | 5. 전체")
    period_choice = input("번호를 입력하세요 (1~5): ").strip()

    mapping = {"1": 7, "2": 30, "3": 90, "4": 180, "5": None}
    days = mapping.get(period_choice, None)

    # =========================
    # Amazon (CSV 기반 + 기간 필터)
    # =========================
    if site_choice == "1":
        print("\n📦 Amazon 리뷰 CSV 불러오는 중...")

        base_dir = os.path.dirname(__file__)
        csv_path = os.path.join(base_dir, "amazon_reviews.csv")

        product_reviews = load_amazon_reviews_by_product(
            csv_path,
            days=days
        )
        source = "Amazon"

    # =========================
    # @COSME
    # =========================
    elif site_choice == "2":
        print("\n📦 @COSME 리뷰 크롤링 중...")
        product_reviews = cosme_crawler.crawl_laneige_reviews(days=days)
        source = "@COSME"

    else:
        print("❌ 잘못된 선택입니다.")
        return

    if not product_reviews:
        print("\n⚠️ 리뷰 데이터가 없습니다.")
        return

    print(f"\n✅ {source} 리뷰 수집 완료! 분석을 시작합니다.")

    for product_name, reviews in product_reviews.items():
        print(f"\n🧬 분석 중: {product_name} ({len(reviews)}건)")
        result = analyze_reviews(product_name, reviews, source)

        print("-" * 50)
        print(result)
        print("-" * 50)


if __name__ == "__main__":
    run_pipeline()
