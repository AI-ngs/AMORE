# main.py : 앱 시작 + 라우터 등록
# FastAPI 앱을 생성하고, 여러 API 라우터를 포함시킴
# 하기 코드는 예시이며 변경될 수 있음

from fastapi import FastAPI
from app.api_products import router as products_router
from app.api_excel import router as excel_router
from app.api_insight import router as insight_router
from app.api_summary import router as summary_router


app = FastAPI(title="AMORE API")

app.include_router(insight_router, prefix="/api")
app.include_router(excel_router, prefix="/api")
app.include_router(products_router, prefix="/api")
app.include_router(summary_router, prefix="/api")
