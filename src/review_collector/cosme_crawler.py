from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from datetime import datetime, timedelta
import time
import re

def parse_cosme_date(text):
    m = re.search(r"(\d{4}/\d{1,2}/\d{1,2})", text)
    return datetime.strptime(m.group(1), "%Y/%m/%d") if m else None

def crawl_by_id(product_id, days=None, max_pages=5):
    reviews = []

    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--lang=ja-JP")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
    )

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    base_url = f"https://www.cosme.net/products/{product_id}/review/"

    try:
        for page in range(1, max_pages + 1):
            driver.get(f"{base_url}?page={page}")
            time.sleep(3)

            # 사람처럼 스크롤
            height = driver.execute_script("return document.body.scrollHeight")
            for y in range(0, height, 300):
                driver.execute_script(f"window.scrollTo(0, {y});")
                time.sleep(0.15)

            items = driver.find_elements(By.CSS_SELECTOR, "div.review-sec")
            if not items:
                break

            page_count = 0

            for item in items:
                try:
                    # ✅ 날짜 (모바일 / PC 분기)
                    r_date = None
                    try:
                        date_text = item.find_element(
                            By.CSS_SELECTOR, "p.mobile-date"
                        ).text
                        r_date = parse_cosme_date(date_text)
                    except:
                        try:
                            date_text = item.find_element(
                                By.CSS_SELECTOR, "p.date"
                            ).text
                            r_date = parse_cosme_date(date_text)
                        except:
                            pass  # 날짜 없음 허용

                    if days and r_date:
                        if r_date < datetime.now() - timedelta(days=days):
                            return reviews

                    # ✅ 리뷰 본문
                    text = item.find_element(By.CSS_SELECTOR, "p.read").text.strip()
                    if text:
                        reviews.append(text)
                        page_count += 1

                except:
                    continue

            print(f"   - {page}페이지 완료 ({page_count}건 / 누적 {len(reviews)}건)")

    finally:
        driver.quit()

    return reviews
