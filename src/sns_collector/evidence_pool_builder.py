import os
import pickle
from typing import List, Dict, Any

import numpy as np
from openai import OpenAI

from youtube_collect import get_youtube_results


# -------------------------
# 임베딩 텍스트 구성
# -------------------------
def build_embedding_text(doc: Dict[str, Any]) -> str:
    comments = doc.get("top_comments", [])
    comments_text = "\n".join([f"- {c.get('text','')}" for c in comments]) if comments else "(no comments)"

    return (
        f"Title: {doc.get('title','')}\n"
        f"Channel: {doc.get('channel','')}\n"
        f"Region: {doc.get('region','')}\n"
        f"SearchQuery: {doc.get('search_query','')}\n"
        f"PublishedAt: {doc.get('published_at','')}\n"
        f"ViewCount: {doc.get('view_count',0)}\n"
        f"URL: {doc.get('video_url','')}\n\n"
        f"Description:\n{doc.get('description','')}\n\n"
        f"TopComments:\n{comments_text}\n"
    )


def build_evidence_pool(
    search_query: str,
    region_code: str
) -> List[Dict[str, Any]]:

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY 환경변수가 설정되지 않았습니다.")

    client = OpenAI(api_key=api_key)

    youtube_results = get_youtube_results(
        search_query=search_query,
        region_code=region_code,
        published_after_days=365,
        min_view_count=2_000,
        max_results=50,
        top_comments_n=3
    )

    evidence_pool = []

    for doc in youtube_results:
        embedding_text = build_embedding_text(doc)

        embedding = client.embeddings.create(
            model="text-embedding-3-small",
            input=embedding_text
        ).data[0].embedding

        evidence_pool.append({
            "embedding": np.array(embedding, dtype=np.float32),
            "doc": doc,
            "embedding_text": embedding_text
        })

    return evidence_pool