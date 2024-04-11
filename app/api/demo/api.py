from fastapi import APIRouter
from app.api.demo.slowqa import qa_slow_api
from app.api.demo.zhipudraw import zhipu_draw
from app.api.demo.yzhk import qa as yzhk_api

api_router = APIRouter()
api_router.include_router(qa_slow_api.router, prefix="/qa_slow", tags=["问答慢速版"])
api_router.include_router(zhipu_draw.router, prefix="/zhipu_draw", tags=["智谱画图"])
api_router.include_router(yzhk_api.router, prefix="/yzhk",  tags=["扬州航空问答DEMO"])


