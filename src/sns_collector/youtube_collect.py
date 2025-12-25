import os
import re
from googleapiclient.discovery import build
from datetime import datetime, timedelta
from typing import List, Dict, Any


# -------------------------
# 언어 판별 함수
# -------------------------
def contains_japanese(text: str) -> bool:
    return bool(re.search(r"[ぁ-んァ-ン一-龯]", text))


def contains_english(text: str) -> bool:
    return bool(re.search(r"[A-Za-z]", text))


def contains_target_language(text: str, region_code: str) -> bool:
    if region_code == "JP":
        return contains_japanese(text)
    elif region_code == "US":
        return contains_english(text)
    else:
        return True


# -------------------------
# 핵심: 유튜브 결과를 "문서 리스트"로 반환
# -------------------------
def get_youtube_results(
    search_query: str,
    region_code: str = "JP",
    published_after_days: int = 365,
    min_view_count: int = 2_000,
    max_results: int = 50,
    top_comments_n: int = 3,
) -> List[Dict[str, Any]]:
    """
    YouTube Data API로 검색 → 영상 상세 조회 → (필터링) → top comments → 문서화 반환
    - 파일 저장 없음 (메모리 변수로만 반환)
    """

    youtube_api_key = os.getenv("YOUTUBE_API_KEY")
    if not youtube_api_key:
        raise RuntimeError("YOUTUBE_API_KEY 환경변수가 설정되지 않았습니다.")

    youtube = build("youtube", "v3", developerKey=youtube_api_key)

    # 검색 범위(기간) 설정
    published_after = (
        datetime.utcnow() - timedelta(days=published_after_days)
    ).isoformat("T") + "Z"

    # 검색 (최신순)
    search_response = youtube.search().list(
        q=search_query,
        part="snippet",
        type="video",
        order="date",
        regionCode=region_code,
        publishedAfter=published_after,
        maxResults=max_results  # 페이지당 최대치(후보 제한 아님)
    ).execute()

    video_ids = [
        item["id"]["videoId"]
        for item in search_response.get("items", [])
        if "id" in item and "videoId" in item["id"]
    ]

    if not video_ids:
        return []

    # 영상 상세 조회
    videos_response = youtube.videos().list(
        part="snippet,statistics",
        id=",".join(video_ids)
    ).execute()

    youtube_results: List[Dict[str, Any]] = []

    for item in videos_response.get("items", []):
        snippet = item.get("snippet", {})
        stats = item.get("statistics", {})

        # 원본값
        video_id = item.get("id")
        if not video_id:
            continue

        title = snippet.get("title", "")
        description = snippet.get("description", "")
        channel = snippet.get("channelTitle", "")
        published_at = snippet.get("publishedAt", "")
        view_count = int(stats.get("viewCount", 0))
        video_url = f"https://www.youtube.com/watch?v={video_id}"

        # 필터 1) 조회수
        if view_count < min_view_count:
            continue

        # 필터 2) 국가별 언어
        if not contains_target_language(title + " " + description, region_code):
            continue

        # 베스트 댓글 N개
        top_comments = []
        try:
            comments_response = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                order="relevance",
                maxResults=top_comments_n,
                textFormat="plainText"
            ).execute()

            for c in comments_response.get("items", []):
                c_snip = c["snippet"]["topLevelComment"]["snippet"]
                top_comments.append({
                    "author": c_snip.get("authorDisplayName", ""),
                    "text": c_snip.get("textDisplay", ""),
                    "like_count": int(c_snip.get("likeCount", 0))
                })
        except Exception:
            # 댓글 비활성화/제한 등
            pass

        # RAG용 문서(메타 포함)
        youtube_result = {
            "video_id": video_id,
            "video_url": video_url,
            "region": region_code,
            "search_query": search_query,
            "published_at": published_at,
            "view_count": view_count,
            "title": title,
            "channel": channel,
            "description": description,
            "top_comments": top_comments
        }

        youtube_results.append(youtube_result)

    return youtube_results


if __name__ == "__main__":
    # 단독 실행 테스트용
    SEARCH_QUERY = "フェイスクリーム"
    REGION_CODE = "JP"
    results = get_youtube_results(
        search_query=SEARCH_QUERY,
        region_code=REGION_CODE,
        published_after_days=365,
        min_view_count=2_000
    )
    print(f"문서 생성 완료: {len(results)}개")
    # 1개만 샘플 출력
    if results:
        print(results[0])
