import requests
import logging
from datetime import datetime
from dotenv import load_dotenv
import os
# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()
app_id = os.getenv('APP_APP_ID')

def submit_drawing_task(token, question, model_id,image_size, username='航空poc', quality='standard'):
    DRAW_TASK_API = f"https://app.dcclouds.com/api/smart/open_api/CODE_SMART_DRAW/add_task/{app_id}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": token
    }
    payload = {
        "question": question,
        "model_id": model_id,
        "username": username,
        "image_size": image_size,
        "quality": quality
    }
    try:
        response = requests.post(DRAW_TASK_API, headers=headers, json=payload, timeout=60, verify=False)
        result = response.json()
        print(result)
        if result.get('code') == 200:
            task_id = result.get("data", {}).get("id")
            logger.info("{} -> Task submitted successfully, ID: {}".format(datetime.now(), task_id))
            return {"code": 200, "id": task_id, "msg": "Success"}
        else:
            logger.info("{} -> Failed to submit drawing task!".format(datetime.now()))
            return {"code": 999, "msg": "Drawing task submission API error" + str(result)}
    except Exception as e:
        logger.error("{} -> Exception occurred: {}".format(datetime.now(), e))
        return {"code": 500, "msg": "Internal server error"+str(e)}


