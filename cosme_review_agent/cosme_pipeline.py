from cosme_crawler import crawl_brand_reviews
from cosme_analyzer import analyze_reviews

def run_pipeline(brand_url):
    all_product_reviews = crawl_brand_reviews(brand_url)
    print("가져온 상품 수:", len(all_product_reviews))

    final_results = {}

    for product_name, reviews in all_product_reviews.items():
        if not reviews:
            continue

        analysis = analyze_reviews(reviews)
        final_results[product_name] = analysis

    return final_results


if __name__ == "__main__":
    print("🔥 pipeline 실행 시작\n")

    results = run_pipeline(
        brand_url="https://www.cosme.net/brands/7623/review/"
    )

    for product, analysis in results.items():
        print(f"🧴 상품명: {product}")

        aspect_analysis = analysis.get("aspect_analysis", {})

        # =========================
        # 속성 분석 출력
        # =========================
        if aspect_analysis:
            for aspect, info in aspect_analysis.items():
                print(f"\n{aspect}:")
                print(f"- 언급 건수: {info['언급_건수']}")

                words = [w for w, _ in info["확장_표현_TOP"]]
                if words:
                    print(f"- 확장 표현: {', '.join(words)}")
                else:
                    print("- 확장 표현: 없음")
        else:
            print("\n속성 기반 분석 데이터가 충분하지 않습니다.")

        # =========================
        # 🔥 총평은 항상 출력
        # =========================
        s = analysis["sentiment_ratio"]
        print(
            f"\n총평: 긍정({s['긍정']}%) "
            f"중립({s['중립']}%) "
            f"부정({s['부정']}%)"
        )

        print("\n" + "-" * 50 + "\n")
