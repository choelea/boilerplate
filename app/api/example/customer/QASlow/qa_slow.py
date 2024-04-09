from fastapi import APIRouter, HTTPException
from app.schemas.message_schema import QaSlowMessage
import logging
from datetime import datetime
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import AzureChatOpenAI
from app.api.example.customer.QASlow import langchain_vectorstores ,langchain_vectorstores_precision
from app.api.example.customer.QASlow import zhipu_ai
from langchain.chains import LLMChain
import serpapi
import os
from dotenv import load_dotenv


# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
load_dotenv()

router = APIRouter()
def checkUrl(question,content,model):
    if model == '严格':
        knowledge = langchain_vectorstores_precision.query_all_matches_precision(question, content)
    elif model == '发散':
        knowledge = langchain_vectorstores.query_all_matches(question, content)
    chat = zhipu_ai.ChatZhipuAI(
        temperature=0.5,
        api_key=os.getenv('zhipu_api_key'),
        model="glm-4",
    )
    # print(knowledge)
    response = chat.invoke("总结，知识：" + str(knowledge) + "\\n问题：" + str(question) + "判断知识和问题有关吗"
                                                                                                "如果判断知识和问题有关则输出例子，将文章中的连接转换成标签，并且只返回标签！！！（标签例子： <p><img src='https://...2.jpg' alt='介绍飞机的机身结构'> </p>可能有多个)\\n"
                                                                                                "如果判断知识和问题关联不大或如果没有连接url 则返回null，不要自己加任何话，只返回null")
    return response.content

def qa(question,content,model):

    if model == '严格':
        knowledge = langchain_vectorstores_precision.query_all_matches_precision(question, content)
    elif model == '发散':
        knowledge = langchain_vectorstores.query_all_matches(question, content)

    # 没有加入环境变量
    llm = AzureChatOpenAI(
        azure_endpoint="https://coe0118.openai.azure.com/",
        azure_deployment="gpt-35-turbo",
        openai_api_version="2023-07-01-preview",
        openai_api_key=os.getenv('AZURE_OPENAI_API_KEY')
    )

    template = """
            你是星小航，一个问答助力.请使用以下检索到的上下文来回答问题，并尽量使用检索到的上下文回答。
            如果上下文中提到“中航机载系统共性技术有限公司”，尽可能让其出现在回答中。
            如果你不知道答案，就说你不知道。
            将内容总结到100字以内，不知道则不用
            Question: {question} 
            Context: {context} 
            Answer:
            """
    template_image = """
                你是星小航，一个专业的客服,请礼貌回答问题。
                用以下检索到的上下文来回答问题，并尽量使用检索到的上下文回答。
                如果问题涉及到‘扬州市航空行业发展’ 相关，请尽量让“中航机载系统共性技术有限公司”，合理出现在回答中。
                如果你在Context中无法获得答案，则用Search回答，并俏皮灵动的回答这个问题参考下面例子。
                将内容总结到100字以内，不知道则不用
                不要说根据上下文之类的思考过程，只说结果
                将内容总结到100字以内
                '''
                问题1（飞机的组成部分是什么？）
                回答例子1(知道结果情况下)：’飞机通常由...‘
                问题2（推荐我吃什么）
                回答例子2(上下文没结果，则猜测)：’不知道你现在的心情和口味偏好，不过我可以给你推荐一些普遍受欢迎的选项。你可以根据自己的喜好来选择：1.中式快餐...‘
                '''
                Question: {question} 
                Context: {context} 
                Search: {search}
                Answer:
                """


    # docs = [Document(text, metadata=None) for text in knowledge]


    if model == '严格':
        #question_temp = "请在文档中查询" + question + "内容，若不存在则回答不存在，若存在请回答存在得具体相关内容，按要求回答给我，不要说根据上下文之类的思考过程"
        prompt = ChatPromptTemplate.from_template(template)
        # return knowledge
    elif model == '发散':
        #question_temp = question
        prompt = ChatPromptTemplate.from_template(template_image)
    else:
        raise HTTPException(status_code=500, detail="Model 参数无效。请选择 '严格' 或 '发散'。")

    question_generator_chain = LLMChain(llm=llm, prompt=prompt)

    #没有加入环境变量
    client = serpapi.Client(api_key=os.getenv('SERP_API_KEY'))
    params1 = {
        "engine": "google",
        "q": question,
        "location": "Hongkou,Shanghai,China",
        "hl": "zh-CN",
        "gl": "cn",
        "output": "json"
    }
    if knowledge == "没有数据":
        results1 = client.search(params1)
        if results1.get("organic_results"):
            first_result = results1["organic_results"][0]  # Access the first result
            search = str(first_result)
        else:
            search = str("No results found.")
    else:
        search = "null"
    res = question_generator_chain.invoke({"question": question, "context": knowledge, "search": search, 'chat_history': ''},
                                          return_only_outputs=False)


    return res

@router.get("/qa_slow")
def qa_route(question: str, model: str, content: str):
    pic = 'null'
    try:

        if model == '严格' or model == '发散':
            model = model
        else:
            code = 500
            result = "模式选择错误"
            msg = "失败"

        if question == 'null':
            code = 500
            result = "请输入问题"
            msg = "失败"

        else:

            result = qa(question,content,model)
            pic = checkUrl(question,content,model)
            code = 200
            result = result
            msg = "成功"
    except Exception as e:
        current_time = datetime.now()
        exception_message = str(e)
        logger.info("{} -> 程序产生异常,信息为: {}".format(current_time, exception_message))
        code = 500
        msg = "服务端内部异常"

    return QaSlowMessage(code=code, result=result, msg=msg, model=model, content=content, pic=pic)

if __name__ == '__main__':
    print(qa_route('我是帅小伙吗','发散','text'))