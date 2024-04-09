from fastapi import APIRouter
from app.api.v1.customer import (
    chat,
    qa,
    yzhk_qa
)

api_router = APIRouter()
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
api_router.include_router(qa.router, prefix="/qa", tags=["qa"])
api_router.include_router(yzhk_qa.router, prefix="/langchain_qa", tags=["航空问答"])

