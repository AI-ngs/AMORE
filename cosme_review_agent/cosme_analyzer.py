from collections import Counter
from sudachipy import dictionary, tokenizer
import re

# ===============================
# 형태소 분석기
# ===============================
tokenizer_obj = dictionary.Dictionary().create()
mode = tokenizer.Tokenizer.SplitMode.C

# ===============================
# 감성 단어 (총평용)
# ===============================
POSITIVE_WORDS = ["良い", "好き", "満足", "おすすめ", "良かった"]
NEGATIVE_WORDS = ["悪い", "不満", "微妙", "合わない"]

# ===============================
# 🔥 강화된 불용어
# ===============================
STOPWORDS = set([
    "する", "ある", "いる", "なる", "思う",
    "これ", "それ", "ため", "ところ", "よう",
    "感じ", "方", "商品", "使用", "購入",
    "今回", "他", "自分", "私", "もの", "場合",
    "現品", "場所", "効果", "関連", "ワード",
    "記事", "紹介", "内容", "情報", "写真",
    "ページ", "レビュー", "投稿", "評価",
    "全体", "印象", "意味", "理由", "結果",
    "とても", "かなり", "少し", "ちょっと"
])

# ===============================
# 속성 + 대표 키워드
# ===============================
ASPECT_ANCHORS = {
    "보습력": ["保湿"],
    "발림성": ["伸び"],
    "지속력": ["持続"],
    "향": ["香り"],
    "색": ["色"],
}

# ===============================
# 문장 분리 함수 (일본어 기준)
# ===============================
def split_sentences(text):
    sentences = re.split(r"[。！？]", text)
    return [s.strip() for s in sentences if len(s.strip()) > 0]

# ===============================
# 리뷰 감성 판별 (총평용)
# ===============================
def get_review_sentiment(text):
    score = 0
    for p in POSITIVE_WORDS:
        if p in text:
            score += 1
    for n in NEGATIVE_WORDS:
        if n in text:
            score -= 1

    if score > 0:
        return "positive"
    elif score < 0:
        return "negative"
    return "neutral"

# ===============================
# 🔥 메인 분석 함수
# ===============================
def analyze_reviews(texts, top_n=5):
    # ---------------------------
    # 1️⃣ 총평 감성 비율
    # ---------------------------
    sentiment_cnt = {"positive": 0, "neutral": 0, "negative": 0}

    for text in texts:
        sentiment_cnt[get_review_sentiment(text)] += 1

    total = sum(sentiment_cnt.values()) or 1

    sentiment_ratio = {
        "긍정": round(sentiment_cnt["positive"] / total * 100, 1),
        "중립": round(sentiment_cnt["neutral"] / total * 100, 1),
        "부정": round(sentiment_cnt["negative"] / total * 100, 1),
    }

    # ---------------------------
    # 2️⃣ 문장 단위 속성 분석
    # ---------------------------
    aspect_analysis = {}

    for aspect, anchors in ASPECT_ANCHORS.items():
        mention_count = 0
        word_counter = Counter()

        for text in texts:
            sentences = split_sentences(text)

            for sentence in sentences:
                if not any(anchor in sentence for anchor in anchors):
                    continue

                mention_count += 1

                for token in tokenizer_obj.tokenize(sentence, mode):
                    pos = token.part_of_speech()[0]
                    base = token.dictionary_form()

                    if pos not in ["名詞", "形容詞"]:
                        continue
                    if base in STOPWORDS:
                        continue
                    if len(base) <= 1:
                        continue

                    word_counter[base] += 1

        if mention_count > 0:
            aspect_analysis[aspect] = {
                "언급_건수": mention_count,
                "확장_표현_TOP": word_counter.most_common(top_n)
            }

    # ---------------------------
    # 3️⃣ 파이프라인 호환 반환
    # ---------------------------
    return {
        "positive_keywords": {},
        "negative_keywords": {},
        "sentiment_ratio": sentiment_ratio,
        "aspect_analysis": aspect_analysis
    }
