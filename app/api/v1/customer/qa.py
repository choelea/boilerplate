from fastapi import APIRouter
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

from app.schemas.message_schema import (
    IUserMessage,
)

output_parser = StrOutputParser()
router = APIRouter()
llm = ChatOpenAI()


@router.get("/get_answer")
async def get_answer(question: str):
    chain = llm | output_parser
    res = chain.invoke(question)
    return IUserMessage(message=res)
