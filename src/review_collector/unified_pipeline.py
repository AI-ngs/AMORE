import csv
import os
from datetime import datetime, timedelta
import cosme_crawler
from unified_analyzer import analyze_reviews


# =========================
# @COSME 제품 정보 로드
# =========================
def load_cosme_info(csv_path):
    info_map = {}

    if not os.path.exists(csv_path):
        print(f"❌ 파일을 찾을 수 없습니다: {csv_path}")
        return info_map

    with open(csv_path, mode="r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            clean_row = {k.strip(): v.strip() for k, v in row.items()}
            if "eng_name" in clean_row and "product_id" in clean_row:
                key = clean_row["eng_name"].lower().replace(" ", "")
                info_map[key] = clean_row["product_id"]

    return info_map


# =========================
# Amazon CSV 리뷰 로드
# =========================
def load_amazon_reviews_by_product(csv_path, target_key, days=None):
    reviews = []

    if not os.path.exists(csv_path):
        print(f"❌ Amazon CSV 파일 없음: {csv_path}")
        return reviews

    # 🔥 인코딩 자동 대응
    encodings = ["utf-8-sig", "cp949", "euc-kr"]

    for enc in encodings:
        try:
            with open(csv_path, mode="r", encoding=enc) as f:
                reader = csv.DictReader(f)

                for row in reader:
                    try:
                        product_name = row["product_name"].strip().lower().replace(" ", "")
                        review_text = row["review_text"].strip()
                        review_date_str = row["review_date"].strip()
                    except Exception:
                        continue

                    if product_name != target_key:
                        continue

                    # 날짜 파싱
                    review_date = None
                    for fmt in ("%Y-%m-%d", "%d-%b-%y", "%Y/%m/%d"):
                        try:
                            review_date = datetime.strptime(review_date_str, fmt)
                            break
                        except:
                            pass

                    if review_date is None:
                        continue

                    if days:
                        if review_date < datetime.now() - timedelta(days=days):
                            continue

                    if review_text:
                        reviews.append(review_text)

            print(f"✅ Amazon CSV 로딩 성공 (encoding={enc})")
            return reviews

        except UnicodeDecodeError:
            continue

    print("❌ Amazon CSV 인코딩을 인식할 수 없습니다.")
    return reviews



# =========================
# 메인 파이프라인
# =========================
def main():
    reviews = []

    print("=== 라네즈 통합 리뷰 분석 시스템 ===")
    print("1. Amazon (CSV) | 2. @COSME (Crawling)")
    site_choice = input("사이트를 선택하세요 (1/2): ").strip()

    print("\n[기간 설정]")
    print("1. 7일 | 2. 30일 | 3. 90일 | 4. 180일 | 5. 전체")
    period_choice = input("번호를 입력하세요 (1~5): ").strip()
    days = {"1": 7, "2": 30, "3": 90, "4": 180, "5": None}.get(period_choice, None)

    target_product_raw = input("\n분석할 제품명(영문)을 입력하세요: ").strip()
    target_key = target_product_raw.lower().replace(" ", "")

    # 항상 이 파일이 있는 폴더 기준
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # =========================
    # Amazon
    # =========================
    if site_choice == "1":
        source = "Amazon"
        csv_path = os.path.join(base_dir, "amazon_reviews.csv")

        reviews = load_amazon_reviews_by_product(
            csv_path,
            target_key,
            days=days
        )

    # =========================
    # @COSME
    # =========================
    elif site_choice == "2":
        source = "@COSME"
        csv_path = os.path.join(base_dir, "cosme_info.csv")

        cosme_info = load_cosme_info(csv_path)
        product_id = cosme_info.get(target_key)

        if not product_id:
            print(f"❌ cosme_info.csv에서 '{target_product_raw}'를 찾을 수 없습니다.")
            print("등록된 제품:", list(cosme_info.keys()))
            return

        print(f"✅ 제품 ID {product_id} 확인됨. 크롤링 시작...")
        reviews = cosme_crawler.crawl_by_id(product_id, days=days)

    else:
        print("❌ 잘못된 선택입니다.")
        return

    # =========================
    # 분석
    # =========================
    if not reviews:
        print("\n❌ 분석할 리뷰 데이터가 없습니다.")
        return

    print(f"\n🚀 분석 시작... (총 {len(reviews)}건)")
    result = analyze_reviews(target_product_raw, reviews, source)

    print("\n" + "=" * 60)
    try:
        print(result)
    except UnicodeEncodeError:
        print(result.encode("utf-8", errors="ignore").decode("utf-8"))
    print("=" * 60)


if __name__ == "__main__":
    main()
