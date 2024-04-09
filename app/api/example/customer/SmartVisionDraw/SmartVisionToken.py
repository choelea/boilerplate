import os
import requests
import logging
from dotenv import load_dotenv
from datetime import datetime

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
load_dotenv()

# 从环境变量读取配置
ak = os.getenv('APP_AK', 'null')
sk = os.getenv('APP_SK', 'null')
app_id = os.getenv('APP_APP_ID', 'null')

TOKEN_API = "https://app.dcclouds.com/api/smart/open_api/token"
CONST_CODE = "code"
CONST_TOKEN = "token"
CONST_MSG = "msg"
APP_ID = "app_id"
def get_token():
    # print(ak)
    # print(sk)
    # print(app_id)

    map = {}
    # 构建请求参数
    params = {
        "ak": ak,
        "sk": sk,
        "app_id": app_id
    }
    try:
        # 发送请求并设置超时为1分钟
        # response = requests.post(TOKEN_API, data=params, timeout=60)
        response = requests.post(TOKEN_API, data=params, timeout=60, verify=False)
        result = response.text
        logger.info("{} -> 接收到响应结果：{}".format(datetime.now(), result))
        result_json = response.json()
        map[APP_ID] = app_id
        if result_json.get(CONST_CODE) == 200:
            token = result_json.get("data", {}).get(CONST_TOKEN, '')
            logger.info("{} -> token获取成功,值为：{}".format(datetime.now(), token))
            map[CONST_CODE] = 200
            map[CONST_TOKEN] = token
            map[CONST_MSG] = "成功"

        else:
            logger.info("{} -> token获取失败!".format(datetime.now()))
            map[CONST_CODE] = 999
            map[CONST_MSG] = "【慧绘图】获取token接口异常" + str(result_json)
    except Exception as e:
        logger.info("{} -> 程序产生异常,信息为: {}".format(datetime.now(), e))
        map[CONST_CODE] = 500
        map[CONST_MSG] = "服务端内部异常"
    return map

