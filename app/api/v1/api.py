from fastapi import APIRouter
from app.api.v1.customer import (
    chat,
)
from app.api.demo.yzhk import qa

api_router = APIRouter()
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
api_router.include_router(qa.router, prefix="/qa", tags=["qa"])

