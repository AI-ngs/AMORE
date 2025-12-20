from cosme_crawler import crawl_reviews_by_product
from cosme_analyzer import analyze_reviews_with_llm

def run_pipeline():
    print("🚀 파이프라인 실행 시작")

    product_reviews = crawl_reviews_by_product()

    for product_name, reviews in product_reviews.items():
        print("\n" + "=" * 50)
        print(f"🧴 제품명: {product_name}")

        result = analyze_reviews_with_llm(product_name, reviews)

        if not result:
            print("❌ 분석 실패")
            continue

        # 속성별 출력
        for attr, data in result["attributes"].items():
            print(f"\n{attr}")
            print(f"- 긍정: {data['positive']}건")
            print(f"- 부정: {data['negative']}건")
            print(f"- {data['summary']}")

        # 총평
        overall = result["overall"]
        print("\n총평:")
        print(f"- 긍정 {overall['positive']}%")
        print(f"- 중립 {overall['neutral']}%")
        print(f"- 부정 {overall['negative']}%")

        # 강점 / 개선
        print("\n강점")
        print(f"- {result['strengths']}")

        print("\n개선 포인트")
        print(f"- {result['weaknesses']}")

if __name__ == "__main__":
    run_pipeline()
