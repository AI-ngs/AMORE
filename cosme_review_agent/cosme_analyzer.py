from openai import OpenAI
import json
import os

# 🔐 API KEY 로드
def load_api_keys(filepath="api_key2.txt"):
    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            if line and "=" in line:
                key, value = line.split("=", 1)
                os.environ[key.strip()] = value.strip()

path = '/Users/User/Desktop/'
# API 키 로드 및 환경변수 설정
load_api_keys(path + 'api_key2.txt')

client = OpenAI()

def analyze_reviews_with_llm(product_name, reviews):
    """
    product_name: str
    reviews: List[str]
    """

    # 리뷰 너무 많으면 비용/속도 문제 → 샘플링
    reviews = reviews[:100]

    prompt = f"""
당신은 화장품 리뷰 분석 전문가입니다.

다음은 하나의 화장품에 대한 리뷰 목록입니다.
리뷰를 분석해서 아래 형식의 JSON으로 결과를 만들어주세요.

[분석 기준]
- 속성: 보습력, 향, 지속력, 발림성 (리뷰에 등장한 것만 사용)
- 각 속성마다 긍정/부정 건수 계산
- 속성별 특징 요약 문장 작성
- 전체 리뷰 기준 총평 비율 계산
- 강점 / 개선 포인트 자연어 요약

[출력 형식(JSON만)]
{{
  "attributes": {{
    "보습력": {{
      "positive": 45,
      "negative": 5,
      "summary": "촉촉하다, 보습이 좋다는 리뷰가 많았고 간혹 건조하다는 평이 있음"
    }}
  }},
  "overall": {{
    "positive": 63,
    "neutral": 12,
    "negative": 25
  }},
  "strengths": "보습력과 지속력에 대해 긍정적인 평가가 많아 건성 피부 사용자에게 적합함",
  "weaknesses": "향에 대한 호불호가 크며 특히 곰팡이향에 대한 부정적 리뷰가 다수 존재함"
}}

[제품명]
{product_name}

[리뷰 목록]
{chr(10).join(reviews)}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    content = response.choices[0].message.content

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        print("❌ JSON 파싱 실패")
        print(content)
        return None
