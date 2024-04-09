from fastapi import APIRouter
from app.api.example.customer.QASlow import qa_slow
from app.api.example.customer.SmartVisionDraw import SmartVision
from app.api.example.customer.ZhiPuDraw import ZhipuDraw

api_router = APIRouter()
api_router.include_router(qa_slow.router, prefix="/qa_slow", tags=["问答慢速版"])
api_router.include_router(SmartVision.router, prefix="/smartvision_draw", tags=["问学画图"])
api_router.include_router(ZhipuDraw.router, prefix="/zhipu_draw", tags=["智谱画图"])


