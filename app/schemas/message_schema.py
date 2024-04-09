from pydantic import BaseModel, field_validator, Field
from app.utils.uuid6 import uuid7
from typing import List, Union, Any

class CogviewResponse(BaseModel):
    code: int
    result: str
    msg: str

class TokenResponse(BaseModel):
    app_id: str
    code: int
    token: str
    msg: str

class ModelInF(BaseModel):
    # 根据实际返回的模型信息结构来定义属性
    modelId: str
    modelName: str
    # 根据您具体返回的模型信息添加更多字段

class ModelResponse(BaseModel):
    code: int
    data: Union[List[ModelInF], List[Any]] = Field(default_factory=list)
    msg: str


class DrawResponse(BaseModel):
    code: int
    id: str = ""
    msg: str

class QueryResponse(BaseModel):
    code: int
    status: int = None  # 假设状态码可能不总是存在
    raw_storage_path: str = None  # 原始存储路径，只有在任务成功时才有
    msg: str
class QaSlowMessage(BaseModel):
    """User message schema."""
    code: Any
    result: Any
    msg: Any
    model: Any
    content: Any
    pic: Any


class QuestionMatching(BaseModel):
    """
    Question Matching schema.
    match 表示是否匹配
    index 标识配置问题的索引； 1 表示第一个问题，2 表示第二个问题；-1表示没有匹配到问题
    """
    match: bool
    index: int = -1

class IUserMessage(BaseModel):
    """User message schema."""

    message: str


class IChatResponse(BaseModel):
    """Chat response schema."""

    id: str
    message_id: str
    sender: str
    message: Any
    type: str
    suggested_responses: list[str] = []

    @field_validator('id')
    @classmethod
    def check_ids(cls, v):
        if v == "" or v is None:
            return str(uuid7())
        return v

    @field_validator("sender")
    def sender_must_be_bot_or_you(cls, v):
        if v not in ["bot", "you"]:
            raise ValueError("sender must be bot or you")
        return v

    @field_validator("type")
    def validate_message_type(cls, v):
        if v not in ["start", "stream", "end", "error", "info"]:
            raise ValueError("type must be start, stream or end")
        return v
