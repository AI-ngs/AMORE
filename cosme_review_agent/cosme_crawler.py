from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time


def crawl_reviews_by_product(max_pages=5):
    """
    return:
    {
        "상품명A": [리뷰1, 리뷰2, ...],
        "상품명B": [...]
    }
    """

    brand_url = "https://www.cosme.net/brands/7623/review/"

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=options)

    product_reviews = {}

    for page in range(1, max_pages + 1):
        page_url = f"{brand_url}?page={page}"
        print(f"\n📄 페이지 수집 중: {page_url}")

        driver.get(page_url)
        time.sleep(3)

        review_blocks = driver.find_elements(By.CSS_SELECTOR, "div.reviewInformation")
        print(f"DEBUG: {page}페이지 리뷰 블록 수 = {len(review_blocks)}")

        # 리뷰 없으면 종료
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

                product_reviews.setdefault(product_name, []).append(review_text)

            except Exception as e:
                print("[WARN] 리뷰 파싱 실패:", e)
                continue

    driver.quit()
    print(f"\nDEBUG: 가져온 상품 수 = {len(product_reviews)}")
    return product_reviews
