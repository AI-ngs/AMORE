# run_insight.py

import os
from openai import OpenAI

from evidence_pool_builder import build_evidence_pool
from insight_rag import find_relevant_evidence, generate_insight


def main():    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
         raise RuntimeError("OPENAI_API_KEY 환경변수가 설정되지 않았습니다.")

    client = OpenAI(api_key=api_key)

    PRODUCT_NAME = "LANEIGE Face Cream"
    SEARCH_QUERY = "フェイスクリーム"
    REGION_CODE = "JP"
    RANK_DIFF = -3   # +면 상승 / -면 하락

    # 1. Evidence Pool 생성
    evidence_pool = build_evidence_pool(
        search_query=SEARCH_QUERY,
        region_code=REGION_CODE
    )
    print(f"Evidence Pool: {evidence_pool}")

    # 2️. 질문 생성
    query = (
        f"{PRODUCT_NAME}의 순위가 최근 상승했습니다."
        if RANK_DIFF > 0
        else f"{PRODUCT_NAME}의 순위가 최근 하락했습니다."
    )

    # 3️. 관련 근거 검색
    top_evidence = find_relevant_evidence(
        client,
        query,
        evidence_pool,
        top_k=5
    )

    # 4️. 인사이트 생성
    insight = generate_insight(
        client,
        PRODUCT_NAME,
        RANK_DIFF,
        top_evidence
    )

    print("\nd인사이트 결과\n")
    print(insight)


if __name__ == "__main__":
    main()
