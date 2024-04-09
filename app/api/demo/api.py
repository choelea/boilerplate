from fastapi import APIRouter
from app.api.demo.draw import zhipu

api_router = APIRouter()
api_router.include_router(zhipu.router, prefix="/draw/zhipu", tags=["绘图"])


