from openai import OpenAI

# OpenAI API Key 입력
client = OpenAI(api_key="API 키 입력")

def analyze_reviews(product_name, reviews, source):
    # 리뷰 요약 전송용 (최대 30개로 제한하여 안정적 분석)
    review_content = "\n".join(reviews[:30])

    prompt = f"""
당신은 {source}의 화장품 리뷰 분석 전문가입니다.
{product_name} 제품에 대한 다음 리뷰들을 분석하여 보고서를 작성하세요.
거짓으로 작성하지 마세요.

1. 키워드 5개 (반드시 한국어 명사형 단어로 추출)
2. 긍정/중립/부정 비율 (%)
3. 강점 및 개선 포인트
4. 전체 리뷰 요약

제품명: {product_name} (출처: {source})
리뷰 수: {len(reviews)}건
{'-'*20}
{review_content}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ 분석 중 오류 발생: {e}"