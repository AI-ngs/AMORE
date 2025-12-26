from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from datetime import datetime, timedelta
from collections import defaultdict
import time
import re

BASE_URL = "https://www.cosme.net/brands/7623/review/"

def parse_cosme_date(date_text):
    # '2024/12/23' 또는 '2024/5/2' 같은 형식을 찾습니다.
    match = re.search(r"(\d{4}/\d{1,2}/\d{1,2})", date_text)
    if match:
        return datetime.strptime(match.group(1), "%Y/%m/%d")
    return None

def crawl_laneige_reviews(days=None, max_pages=5):
    product_reviews = defaultdict(list)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    for page in range(1, max_pages + 1):
        url = f"{BASE_URL}?page={page}"
        print(f"📄 @COSME {page}페이지 수집 시작...")
        driver.get(url)
        time.sleep(3)

        # 원본 코드의 리뷰 블록 선택자
        review_items = driver.find_elements(By.CSS_SELECTOR, "div.reviewInformation")
        
        if not review_items:
            print("🔎 리뷰 블록을 찾을 수 없어 종료합니다.")
            break

        for item in review_items:
            try:
                # [중요 수정] 날짜 태그를 p.reviewDate로 변경
                try:
                    date_text = item.find_element(By.CSS_SELECTOR, "p.reviewDate").text
                    review_date = parse_cosme_date(date_text)
                except:
                    # 날짜 태그가 없거나 다를 경우를 대비
                    review_date = None

                # 기간 필터링 로직
                if days is not None and review_date:
                    if review_date < datetime.now() - timedelta(days=days):
                        continue # 설정 기간보다 오래된 리뷰면 건너뜀

                # 제품명 및 리뷰 텍스트 (원본 로직 유지)
                product_name = item.find_element(By.CSS_SELECTOR, "h3 a").text.strip()
                review_text = item.find_element(By.CSS_SELECTOR, "div.reviewTxt").text.strip()

                if product_name and review_text:
                    product_reviews[product_name].append(review_text)
            except Exception as e:
                continue

    driver.quit()
    return product_reviews