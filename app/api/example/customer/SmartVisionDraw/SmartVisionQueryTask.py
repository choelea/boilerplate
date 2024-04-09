import requests
import os
import logging
from datetime import datetime
from dotenv import load_dotenv
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
load_dotenv()

app_id = os.getenv('APP_APP_ID', 'null')



def query_drawing_task_status(token, task_id):
    headers = {
        "Content-Type": "application/json",
        "Authorization": token
    }
    params = {
        "id": task_id
    }
    try:
        response = requests.get(f"https://app.dcclouds.com/api/smart/open_api/CODE_SMART_DRAW/query_task/{app_id}", headers=headers, params=params, timeout=60, verify=False)
        result = response.json()
        logger.info("{} -> Received response: {}".format(datetime.now(), result))

        if result.get('code') == 200:
            task_info = result.get('data', {})
            status = task_info.get('status')
            if status == 3:  # Task succeeded
                raw_storage_path = task_info.get('raw_storage_path')
                return {
                    "code": 200,
                    "status": status,
                    "raw_storage_path": raw_storage_path,
                    "msg": "Success"
                }
            else:
                return {
                    "code": 200,
                    "status": status,
                    "msg": "Task in progress or not started"
                }
        else:
            return {"code": result.get('code'), "msg": "Failed to query task status"}
    except Exception as e:
        logger.error("{} -> Exception occurred: {}".format(datetime.now(), e))
        return {"code": 500, "msg": "Internal server error"}




