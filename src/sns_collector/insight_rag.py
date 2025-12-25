# insight_rag.py

import numpy as np
from openai import OpenAI


def find_relevant_evidence(
    client: OpenAI,
    query: str,
    evidence_pool: list,
    top_k: int = 5
):
    q_emb = client.embeddings.create(
        model="text-embedding-3-small",
        input=query
    ).data[0].embedding

    q_emb = np.array(q_emb)

    scored = []
    for item in evidence_pool:
        emb = item["embedding"]
        score = np.dot(q_emb, emb) / (
            np.linalg.norm(q_emb) * np.linalg.norm(emb)
        )
        scored.append((score, item))

    scored.sort(reverse=True, key=lambda x: x[0])
    return [item for _, item in scored[:top_k]]


def generate_insight(
    client: OpenAI,
    product_name: str,
    rank_diff: int,
    evidence_items: list
) -> str:

    trend = "상승" if rank_diff > 0 else "하락"

    evidence_text = "\n\n".join([
        f"""
제목: {e['doc']['title']}
채널: {e['doc']['channel']}
조회수: {e['doc']['view_count']}
URL: {e['doc']['video_url']}
댓글:
""" + "\n".join(
            [f"- {c['text']}" for c in e['doc']['top_comments']]
        )
        for e in evidence_items
    ])

    prompt = f"""
당신은 화장품 시장 분석가입니다.

제품: {product_name}
순위 변화: {trend}

아래 유튜브 콘텐츠 근거만 사용하여
왜 순위가 {trend}했는지 분석하세요.

[근거 콘텐츠]
{evidence_text}

[출력 형식]
- 핵심 요약 1줄
- 상세 분석 (3~5줄)
- 댓글 기반 소비자 반응
- 결론
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content
