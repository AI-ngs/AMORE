from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time


def crawl_brand_reviews(brand_url, max_pages=10):
    """
    brand_url : 브랜드 리뷰 기본 URL
    max_pages : 몇 페이지까지 수집할지 (1페이지당 약 20개 리뷰)
    """

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=options)

    product_reviews = {}

    for page in range(1, max_pages + 1):
        page_url = f"{brand_url}?page={page}"
        print(f"\n📄 페이지 수집 중: {page_url}")

        driver.get(page_url)
        time.sleep(3)

        review_blocks = driver.find_elements(By.CSS_SELECTOR, "div.reviewInformation")
        print(f"DEBUG: {page}페이지 리뷰 블록 수 = {len(review_blocks)}")

        # 리뷰가 없으면 더 이상 페이지 없음
        if len(review_blocks) == 0:
            print("⚠️ 더 이상 리뷰 없음 → 종료")
            break

        for block in review_blocks:
            try:
                # 리뷰 텍스트
                review_text = block.find_element(
                    By.CSS_SELECTOR, "div.reviewTxt"
                ).text.strip()

                if len(review_text) < 5:
                    continue

                # 상품명
                product_name = block.find_element(
                    By.CSS_SELECTOR, "div.productInformation h3 a"
                ).text.strip()

                if product_name not in product_reviews:
                    product_reviews[product_name] = []

                product_reviews[product_name].append(review_text)

            except Exception as e:
                print("[WARN] 리뷰 파싱 실패:", e)
                continue

    driver.quit()
    return product_reviews


# 단독 실행 테스트용
if __name__ == "__main__":
    reviews = crawl_brand_reviews(
        "https://www.cosme.net/brands/7623/review/",
        max_pages=5
    )

    print("\n===== 수집 결과 =====")
    for product, revs in reviews.items():
        print(f"{product}: {len(revs)}개 리뷰")
        if revs:
            print("샘플:", revs[0][:80], "...")
