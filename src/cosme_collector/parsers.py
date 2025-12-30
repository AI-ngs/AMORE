from __future__ import annotations

import re
from bs4 import BeautifulSoup


def absolutize(href: str | None) -> str | None:
    if not href:
        return None
    href = href.strip()
    if href.startswith("//"):
        return "https:" + href
    if href.startswith("/"):
        return "https://www.cosme.net" + href
    return href


def pick_img_url(img) -> str | None:
    if not img:
        return None

    cand = img.get("data-src") or img.get("src")
    if cand:
        return absolutize(cand)

    srcset = img.get("srcset")
    if srcset:
        last = srcset.split(",")[-1].strip().split(" ")[0].strip()
        return absolutize(last)

    return None

def extract_rank_change_text(block) -> str | None:
    """
    @cosme 랭킹 블록에서 순위 변동 텍스트 추출
    우선순위:
    1) dt span.status img alt/title
    2) span.status 안 텍스트
    3) 아이콘 src 파일명(ico_up/down/stay/new) 매핑
    """
    status_span = block.select_one("dt span.status") or block.select_one("span.status")
    if not status_span:
        return None

    img = status_span.select_one("img")
    if img:
        alt = (img.get("alt") or "").strip()
        title = (img.get("title") or "").strip()
        if alt:
            return alt
        if title:
            return title

        src = (img.get("src") or "").lower()
        if "ico_stay" in src:
            return "順位変わらず"
        if "ico_up" in src:
            return "順位上昇"
        if "ico_down" in src:
            return "順位下降"
        if "ico_new" in src:
            return "NEW"

    txt = status_span.get_text(" ", strip=True)
    return txt or None


def parse_product_block(block) -> dict:
    a = block.select_one("dd.pic a[href*='/products/']")
    if not a:
        return {}

    product_url = absolutize(a.get("href"))

    rank_change_text = extract_rank_change_text(block)

    # product_id
    product_id = None
    if product_url:
        m = re.search(r"/products/(\d+)/", product_url)
        if m:
            product_id = m.group(1)

    # 상품명 (img alt가 가장 정확)
    product_name = None
    img = a.select_one("img")
    if img:
        product_name = img.get("alt")

    # 상품 이미지
    image_url = None
    if img:
        image_url = img.get("src") or img.get("data-src")
        image_url = absolutize(image_url)

    # brand
    brand_name = None
    brand_url = None
    brand_a = block.select_one("dd.summary span.brand a[href]")
    if brand_a:
        brand_name = brand_a.get_text(strip=True)
        brand_url = absolutize(brand_a.get("href"))

    # rating
    rating_score = None
    rating_el = block.select_one("p.rating")
    if rating_el:
        try:
            rating_score = float(rating_el.get_text(strip=True))
        except:
            pass

    # review count
    review_count = None
    review_a = block.select_one("p.votes a.count")
    if review_a:
        review_count = int(re.sub(r"\D", "", review_a.get_text()))

    # price
    price_text = None
    price_el = block.select_one("p.price")
    if price_el:
        price_text = price_el.get_text(" ", strip=True)

    return {
        "product_id": product_id,
        "product_name": product_name,
        "product_url": product_url,
        "brand_name": brand_name,
        "brand_url": brand_url,
        "rating_score": rating_score,
        "review_count": review_count,
        "price_text": price_text,
        "image_url": image_url,  # 오직 상품 이미지
        "rank_change_text": rank_change_text,
    }

def parse_page_items_ordered(html: str, limit: int = 10) -> list[dict]:
    soup = BeautifulSoup(html, "lxml")
    items: list[dict] = []

    blocks = soup.select("dl.top3, dl.clearfix")
    for b in blocks:
        row = parse_product_block(b)
        if row.get("product_id"):
            items.append(row)

    # fallback: products 링크 주변 블록 기반
    if not items:
        seen = set()
        for a in soup.select('a[href*="/products/"]'):
            block = a.find_parent(["dl", "li", "article", "section", "div"])
            if not block:
                continue
            k = id(block)
            if k in seen:
                continue
            seen.add(k)

            row = parse_product_block(block)
            if row.get("product_id"):
                items.append(row)

    return items[:limit]


def parse_grouped_keyword_ranking(html: str, max_each_group: int = 3) -> list[dict]:
    soup = BeautifulSoup(html, "lxml")
    rows: list[dict] = []

    heads = soup.select("div.keyword-ranking-head")
    for head in heads:
        h4 = head.select_one("h4")
        group_value = h4.get_text(strip=True) if h4 else None
        if not group_value:
            continue

        items = []
        node = head
        while True:
            node = node.find_next_sibling()
            if node is None:
                break
            cls = node.get("class") or []
            if "keyword-ranking-head" in cls:
                break
            if "keyword-ranking-item" in cls:
                items.append(node)
            if len(items) >= max_each_group:
                break

        for idx, item_block in enumerate(items, start=1):
            prod = parse_product_block(item_block)
            if not prod.get("product_id"):
                continue
            rows.append({"group_value": group_value, "group_rank": idx, **prod})

    return rows
