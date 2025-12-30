from __future__ import annotations


def build_jobs(test_mode: bool = False) -> list[dict]:
    # =========================
    # TEST MODE 10개만 수집
    # =========================
    if test_mode:
        return [
            {
                "source": "cosme",
                "market": "JP",
                "category_id": "ALL",
                "category_name": "종합 뷰티",
                "ranking_type": "products_top100",
                "kind": "topN_pages",
                "page_size": 10,
                "target_n": 10,
                "urls": [
                    "https://www.cosme.net/ranking/products",
                ],
            },
        ]

    # =========================
    # PROD MODE
    # =========================
    return [
        # -------------------------
        # 종합 뷰티 Top100
        # -------------------------
        {
            "source": "cosme",
            "market": "JP",
            "category_id": "ALL",
            "category_name": "종합 뷰티",
            "ranking_type": "products_top100",
            "kind": "topN_pages",
            "page_size": 10,
            "target_n": 100,
            "urls": [
                "https://www.cosme.net/ranking/products",
                "https://www.cosme.net/ranking/products/page/1",
                "https://www.cosme.net/ranking/products/page/2",
                "https://www.cosme.net/ranking/products/page/3",
                "https://www.cosme.net/ranking/products/page/4",
                "https://www.cosme.net/ranking/products/page/5",
                "https://www.cosme.net/ranking/products/page/6",
                "https://www.cosme.net/ranking/products/page/7",
                "https://www.cosme.net/ranking/products/page/8",
                "https://www.cosme.net/ranking/products/page/9",
            ],
        },

        # -------------------------
        # 카테고리: 800 스킨케어
        # -------------------------
        {
            "source": "cosme",
            "market": "JP",
            "category_id": "800",
            "category_name": "종합 스킨케어",
            "ranking_type": "latest_review_top50",
            "kind": "topN_query_pages",
            "page_param": "page",
            "page_size": 10,
            "target_n": 50,
            "urls": [
                "https://www.cosme.net/categories/item/800/ranking/",
                "https://www.cosme.net/categories/item/800/ranking/?page=2",
                "https://www.cosme.net/categories/item/800/ranking/?page=3",
                "https://www.cosme.net/categories/item/800/ranking/?page=4",
                "https://www.cosme.net/categories/item/800/ranking/?page=5",
            ],
        },
        {
            "source": "cosme",
            "market": "JP",
            "category_id": "800",
            "category_name": "종합 스킨케어",
            "ranking_type": "rise_review_top10",
            "kind": "rise",
            "urls": ["https://www.cosme.net/categories/item/800/ranking-rise/"],
        },
        {
            "source": "cosme",
            "market": "JP",
            "category_id": "800",
            "category_name": "종합 스킨케어",
            "ranking_type": "age_top3",
            "kind": "grouped",
            "group_type": "age",
            "urls": ["https://www.cosme.net/categories/item/800/ranking-age/"],
        },
        {
            "source": "cosme",
            "market": "JP",
            "category_id": "800",
            "category_name": "종합 스킨케어",
            "ranking_type": "skin_top3",
            "kind": "grouped",
            "group_type": "skin",
            "urls": ["https://www.cosme.net/categories/item/800/ranking-skin/"],
        },
        {
            "source": "cosme",
            "market": "JP",
            "category_id": "800",
            "category_name": "종합 스킨케어",
            "ranking_type": "pchannel_top3",
            "kind": "grouped",
            "group_type": "pchannel",
            "urls": ["https://www.cosme.net/categories/item/800/ranking-pchannel/"],
        },

        # -------------------------
        # 카테고리: 1005 페이셜크림
        # -------------------------
        {
            "source": "cosme",
            "market": "JP",
            "category_id": "1005",
            "category_name": "페이셜크림",
            "ranking_type": "latest_review_top50",
            "kind": "topN_query_pages",
            "page_param": "page",
            "page_size": 10,
            "target_n": 50,
            "urls": [
                "https://www.cosme.net/categories/item/1005/ranking/",
                "https://www.cosme.net/categories/item/1005/ranking/?page=2",
                "https://www.cosme.net/categories/item/1005/ranking/?page=3",
                "https://www.cosme.net/categories/item/1005/ranking/?page=4",
                "https://www.cosme.net/categories/item/1005/ranking/?page=5",
            ],
        },
        {
            "source": "cosme",
            "market": "JP",
            "category_id": "1005",
            "category_name": "페이셜크림",
            "ranking_type": "rise_review_top10",
            "kind": "rise",
            "urls": ["https://www.cosme.net/categories/item/1005/ranking-rise/"],
        },
        {
            "source": "cosme",
            "market": "JP",
            "category_id": "1005",
            "category_name": "페이셜크림",
            "ranking_type": "age_top3",
            "kind": "grouped",
            "group_type": "age",
            "urls": ["https://www.cosme.net/categories/item/1005/ranking-age/"],
        },
        {
            "source": "cosme",
            "market": "JP",
            "category_id": "1005",
            "category_name": "페이셜크림",
            "ranking_type": "skin_top3",
            "kind": "grouped",
            "group_type": "skin",
            "urls": ["https://www.cosme.net/categories/item/1005/ranking-skin/"],
        },
        {
            "source": "cosme",
            "market": "JP",
            "category_id": "1005",
            "category_name": "페이셜크림",
            "ranking_type": "pchannel_top3",
            "kind": "grouped",
            "group_type": "pchannel",
            "urls": ["https://www.cosme.net/categories/item/1005/ranking-pchannel/"],
        },
        {
            "source": "cosme",
            "market": "JP",
            "category_id": "1005",
            "category_name": "페이셜크림",
            "ranking_type": "cross_top2",
            "kind": "grouped",
            "group_type": "cross",
            "urls": ["https://www.cosme.net/categories/item/1005/ranking-cross/"],
        },

        # -------------------------
        # 카테고리: 904 페이셜마스크
        # -------------------------
        {
            "source": "cosme",
            "market": "JP",
            "category_id": "904",
            "category_name": "페이셜마스크",
            "ranking_type": "latest_review_top50",
            "kind": "topN_query_pages",
            "page_param": "page",
            "page_size": 10,
            "target_n": 50,
            "urls": [
                "https://www.cosme.net/categories/item/904/ranking/",
                "https://www.cosme.net/categories/item/904/ranking/?page=2",
                "https://www.cosme.net/categories/item/904/ranking/?page=3",
                "https://www.cosme.net/categories/item/904/ranking/?page=4",
                "https://www.cosme.net/categories/item/904/ranking/?page=5",
            ],
        },
        {
            "source": "cosme",
            "market": "JP",
            "category_id": "904",
            "category_name": "페이셜마스크",
            "ranking_type": "rise_review_top10",
            "kind": "rise",
            "urls": ["https://www.cosme.net/categories/item/904/ranking-rise/"],
        },
        {
            "source": "cosme",
            "market": "JP",
            "category_id": "904",
            "category_name": "페이셜마스크",
            "ranking_type": "age_top3",
            "kind": "grouped",
            "group_type": "age",
            "urls": ["https://www.cosme.net/categories/item/904/ranking-age/"],
        },
        {
            "source": "cosme",
            "market": "JP",
            "category_id": "904",
            "category_name": "페이셜마스크",
            "ranking_type": "skin_top3",
            "kind": "grouped",
            "group_type": "skin",
            "urls": ["https://www.cosme.net/categories/item/904/ranking-skin/"],
        },
        {
            "source": "cosme",
            "market": "JP",
            "category_id": "904",
            "category_name": "페이셜마스크",
            "ranking_type": "pchannel_top3",
            "kind": "grouped",
            "group_type": "pchannel",
            "urls": ["https://www.cosme.net/categories/item/904/ranking-pchannel/"],
        },

        # -------------------------
        # 카테고리: 803 베이스메이크업
        # -------------------------
        {
            "source": "cosme",
            "market": "JP",
            "category_id": "803",
            "category_name": "베이스메이크업",
            "ranking_type": "latest_review_top50",
            "kind": "topN_query_pages",
            "page_param": "page",
            "page_size": 10,
            "target_n": 50,
            "urls": [
                "https://www.cosme.net/categories/item/803/ranking/",
                "https://www.cosme.net/categories/item/803/ranking/?page=2",
                "https://www.cosme.net/categories/item/803/ranking/?page=3",
                "https://www.cosme.net/categories/item/803/ranking/?page=4",
                "https://www.cosme.net/categories/item/803/ranking/?page=5",
            ],
        },
        {
            "source": "cosme",
            "market": "JP",
            "category_id": "803",
            "category_name": "베이스메이크업",
            "ranking_type": "rise_review_top10",
            "kind": "rise",
            "urls": ["https://www.cosme.net/categories/item/803/ranking-rise/"],
        },
        {
            "source": "cosme",
            "market": "JP",
            "category_id": "803",
            "category_name": "베이스메이크업",
            "ranking_type": "age_top3",
            "kind": "grouped",
            "group_type": "age",
            "urls": ["https://www.cosme.net/categories/item/803/ranking-age/"],
        },
        {
            "source": "cosme",
            "market": "JP",
            "category_id": "803",
            "category_name": "베이스메이크업",
            "ranking_type": "skin_top3",
            "kind": "grouped",
            "group_type": "skin",
            "urls": ["https://www.cosme.net/categories/item/803/ranking-skin/"],
        },
        {
            "source": "cosme",
            "market": "JP",
            "category_id": "803",
            "category_name": "베이스메이크업",
            "ranking_type": "pchannel_top3",
            "kind": "grouped",
            "group_type": "pchannel",
            "urls": ["https://www.cosme.net/categories/item/803/ranking-pchannel/"],
        },
    ]