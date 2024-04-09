import os
import requests
import logging
from datetime import datetime
from dotenv import load_dotenv
# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
load_dotenv()

MODEL_INFO_API = "https://app.dcclouds.com/api/smart/open_api/model_info/"
CONST_CODE = "code"
CONST_DATA = "data"
CONST_MSG = "msg"

# 请确保在环境变量中正确设置了APP_APP_ID和TOKEN



def get_model(token):
    app_id = os.getenv('APP_APP_ID')
    headers = {
        "Content-Type": "application/json",
        "Authorization": token
    }

    try:
        # 发送请求并设置超时为1分钟
        response = requests.get(MODEL_INFO_API + app_id, headers=headers, timeout=60, verify=False)
        result = response.text
        logger.info("{} -> 接收到模型信息响应结果：{}".format(datetime.now(), result))
        result_json = response.json()
        if result_json.get(CONST_CODE) == 200:
            model_info_list = result_json.get(CONST_DATA, [])
            logger.info("{} -> 模型信息获取成功,详情为：{}".format(datetime.now(), model_info_list))
            return {
                CONST_CODE: 200,
                CONST_DATA: model_info_list,
                CONST_MSG: "成功"
            }
        else:
            logger.info("{} -> 模型信息获取失败!".format(datetime.now()))
            return {
                CONST_CODE: result_json.get(CONST_CODE, 999),
                CONST_MSG: "获取模型信息接口异常" + str(result_json.get(CONST_MSG, ''))
            }
    except Exception as e:
        logger.info("{} -> 程序产生异常,信息为: {}".format(datetime.now(), e))
        return {
            CONST_CODE: 500,
            CONST_MSG: "服务端内部异常"+str(e)
        }

