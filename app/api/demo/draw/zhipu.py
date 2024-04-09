from fastapi import FastAPI, APIRouter, Query
import os
from app.schemas.message_schema import CogviewResponse
from zhipuai import ZhipuAI

app = FastAPI()
router = APIRouter()

client = ZhipuAI()


@router.get("")
async def draw(question: str = Query(default='绘制一张小猫钓鱼的图片', description="Question for the AI model")):
    try:
        # 这里假设您有一个客户端类来调用API
        response = client.images.generations(
            model="cogview-3",
            prompt=question,
        )
        return CogviewResponse(code=200, result=response.data[0].url, msg="成功")
    except Exception as e:
        return CogviewResponse(code=500, result=str(e), msg="服务端内部异常")
