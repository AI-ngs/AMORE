import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from cosme_config import HEADERS, DATE_RANGE_MAP

def crawl_reviews(product_url, period):
    """
    product_url: @COSME 상품 상세 페이지
    period: 하루 / 일주일 / 한달 / 3개월 / 6개월 / 전체
    """
    reviews = []
    limit_days = DATE_RANGE_MAP[period]

    response = requests.get(product_url, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")

    review_blocks = soup.select(".review")  # 실제 클래스는 확인 필요

    for block in review_blocks:
        text = block.select_one(".review__text").get_text(strip=True)
        date_text = block.select_one(".review__date").get_text(strip=True)

        review_date = datetime.strptime(date_text, "%Y.%m.%d")

        if limit_days:
            if review_date < datetime.now() - timedelta(days=limit_days):
                continue

        reviews.append({
            "date": review_date,
            "text": text
        })

    return reviews