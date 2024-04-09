from fastapi import FastAPI, APIRouter, Query
import os
from app.schemas.message_schema import CogviewResponse
from zhipuai import ZhipuAI
from dotenv import load_dotenv

app = FastAPI()
router = APIRouter()

@router.get("/cogview", response_model=CogviewResponse)
async def cogview_route(question: str = Query(default='null', description="Question for the AI model")):
    try:
        # 这里假设您有一个客户端类来调用API
        client = ZhipuAI(api_key=os.getenv('zhipu_api_key'))
        response = client.images.generations(
           model="cogview-3",
           prompt=question + "（图片比例16：9）",
        )
        return CogviewResponse(code=200, result=response.data[0].url, msg="成功")
    except Exception as e:
        return CogviewResponse(code=500, result=str(e), msg="服务端内部异常")