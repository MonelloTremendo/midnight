from sqlalchemy import text

from database.connection import get_db
from database.models import Flag, FlagStatus

from config.config import get_config

import requests
import time
import random

def submit_loop():
    connection = next(get_db())
    config = get_config()

    while True:
        flags = 1connection.execute(text("SELECT * FROM flags WHERE status = 0 LIMIT 100")).fetchall()
        flags = [Flag.from_orm(flag) for flag in flags]

        try:
            response = requests.put(config['CHECKSYSTEM_URL'], headers={'X-Team-Token': config['CHECKSYSTEM_TOKEN']}, json=[item.flag for item in flags], timeout=5).json()

            for flag in response:
                connection.execute(text("UPDATE flags SET status = :status, checksystem_response = :response WHERE flag = :flag"), {"status": FlagStatus.ACCEPTED.value if flag.status else FlagStatus.REJECTED.value, "flag": flag.flag, "response": flag.msg})

            connection.commit()
            time.sleep(10)
        except:
            pass