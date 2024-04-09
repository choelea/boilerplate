from fastapi import FastAPI, APIRouter, Query
from app.schemas.message_schema import TokenResponse,ModelResponse,DrawResponse,QueryResponse
from app.api.example.customer.SmartVisionDraw import SmartVisionToken,GetSmartVisionModel,SmartVisionDraw,SmartVisionQueryTask

from dotenv import load_dotenv

app = FastAPI()
router = APIRouter()
load_dotenv()


@router.get("/get_token", response_model=TokenResponse)
async def token_route():
    token_response = SmartVisionToken.get_token()
    return TokenResponse(**token_response)

@router.get("/get_model", response_model=ModelResponse)
async def model_route(token: str = Query(default='null')):
    model = GetSmartVisionModel.get_model(token)
    return ModelResponse(**model)

@router.get("/draw", response_model=DrawResponse)
async def draw_route(token: str, question: str, model_id: str = '702b95fe5cf4e24df7eb9a403b7d0e15', image_size: str = '1024x1024'):
    drwa_result = SmartVisionDraw.submit_drawing_task(token, question, model_id, image_size)
    return DrawResponse(**drwa_result)

@router.get("/get_query", response_model=QueryResponse)
async def get_query(token: str = Query(default='null'), task_id: str = Query(default='null')):
    task_status_info = SmartVisionQueryTask.query_drawing_task_status(token, task_id)
    if 'status' in task_status_info and task_status_info['status'] == 3:
        # 如果任务成功，我们假设返回的字典包含 'raw_storage_path'
        return QueryResponse(code=200, status=task_status_info['status'],
                             raw_storage_path=task_status_info.get('raw_storage_path', ''), msg=task_status_info['msg'])
    else:
        # 任务正在进行中、尚未开始或失败
        return QueryResponse(code=task_status_info['code'], status=task_status_info.get('status', 0),
                             msg=task_status_info['msg'])


