import logging
import os

from fastapi import APIRouter
from langchain_core.output_parsers import StrOutputParser
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import AzureChatOpenAI
from langchain_openai import ChatOpenAI
from app.core.config import settings
from app.schemas.message_schema import QuestionMatching
from app.schemas.response_schema import (
    ICommonRes,
    AnswerResult
)

root_directory = os.getcwd()
qa_1_path = os.path.join(root_directory, 'docs', 'qa_1.html')
qa_2_path = os.path.join(root_directory, 'docs', 'qa_2.html')
with open(qa_1_path, "r", encoding="utf-8") as f:
    qa_1_context = f.read()

with open(qa_2_path, "r", encoding="utf-8") as f:
    qa_2_context = f.read()

private_contexts = [qa_1_context, qa_2_context]
# private_contexts = qa_1_context + qa_2_context
output_parser = StrOutputParser()
json_output_parser = JsonOutputParser()
router = APIRouter()
chatOpenAI = ChatOpenAI(temperature=0)
azureChatOpenAI = AzureChatOpenAI(
    temperature=0,
    azure_endpoint="https://coe0118.openai.azure.com/",
    azure_deployment="gpt-35-turbo",
    openai_api_version="2023-07-01-preview",
    openai_api_key=settings.AZURE_OPENAI_API_KEY
)
llm = azureChatOpenAI
public_template = "你是星小航，在回答问题的时候，保证回到在100字以内。 Question: {question}"
private_template = """
                你是星小航，一个专业的客服,请礼貌简明的回答问题。
                用以下检索到的上下文来回答问题，如果上下文中有提到“中航机载系统共性技术有限公司”，请尽量让“中航机载系统共性技术有限公司”，合理出现在回答中。
                务必将回答限制在150个文字以内。
                Question: {question} 
                Context: {context} 
                """

private_prompt = ChatPromptTemplate.from_template(private_template)
public_promote = ChatPromptTemplate.from_template(public_template)

# 航空私域问答链路
private_chain = private_prompt | llm | output_parser

# 公域问答链路
public_chain = public_promote | llm | output_parser


@router.get("")
async def get_answer(question: str):
    question_matching = await question_match(question)
    logging.info(f"question_matching: {question_matching}")
    if question_matching.match:
        logging.info(f"Going to answer based on private context")
        context = private_contexts[question_matching.index - 1]
        # context = private_contexts
        res = private_chain.invoke({"question": question, "context": context})
    else:
        logging.info(f"Going to answer based on AI's Knowledge")
        res = public_chain.invoke({"question": question})
    logging.info(f"question:{question}, Answer: {res}")
    result = AnswerResult(text=res)
    return ICommonRes[AnswerResult](result=result)


@router.get("/match")
async def is_match(question: str):
    question_matching = await question_match(question)
    return question_matching


async def question_match(question: str) -> QuestionMatching:
    """
    通过大模型判断问题是否和预设的问题列表相同，返回JSON格式{match, index}
    :param question:
    :return:QuestionMatching
    """

    # msg = f"""
    # 判断提问: {question} 是否能在下面'问题列表'中找到匹配项,列表中的问题里的单引号部分是重点且必要匹配点；找出一个匹配项就可以返回；请用JSON格式返回，JSON对象有两个属性：match和index:
    # match: 为true则问题列表中存在和提问匹配的问题，false则表示没有;
    # index: 表示匹配到的第一个问题的序号; 如果没有匹配上则index字段为-1；
    # 问题列表:
    # 1. '扬州市'的'航空'产业
    # 2. '飞机''组成'部分
    # """

    match_chain = llm | json_output_parser
    msg = f"""
    请帮忙判断提问(Question)是否能在给定的问题列表(Question List)找到匹配的；注意问题必须和航空有关联，如果没有视为不匹配； 同义词视为匹配，不要让标点符号影响匹配结果。
    用JSON格式返回，返回对象只需要包含两个字段： match、index。 match表示是否匹配到；index表示匹配到的问题序号，未匹配到的时候index=-1
    
    Question: {question}
    Question List:
    1、扬州航空产业发展如何；
    2、飞机组成部分；
    """

    # msg = f"""
    # 判断提问: {question} 是否和 '扬州航空产业'或'飞机组成部分'相关；请用JSON格式返回，如果相关请返回match字段为true,如果关系不大请返回match为false;
    # 备注：如果问到航空相关的，必须提到扬州或者和扬州市其他相关说法才算相关。
    # """
    res = match_chain.invoke(msg)
    logging.info(f"question_match raw: {res}")
    try:
        return QuestionMatching.model_validate(res)
    except Exception as exc:
        logging.error(f"An error occurred: {exc}")
        return QuestionMatching(match=False, index=-1)
