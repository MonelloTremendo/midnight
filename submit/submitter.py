from sqlalchemy import text

from database.connection import get_db
from database.models import Flag, FlagStatus

from config.config import get_config

import requests
import time

def submit_loop():
    connection = next(get_db())
    config = get_config()

    while True:
        flags = connection.execute(text("SELECT * FROM flags WHERE status = 0 LIMIT 100")).fetchall()
        flags = [Flag.from_orm(flag) for flag in flags]

        print(flags)

        try:
            time.sleep(15)
            response = requests.put(config['CHECKSYSTEM_URL'], headers={'X-Team-Token': config['CHECKSYSTEM_TOKEN']}, json=[item.flag for item in flags], timeout=5)
            print(response.status_code)
            print(response.text)

            flags = response.json()
            print(flags)
            if response.status_code == 200:
                for flag in flags:
                    print(flag)
                    connection.execute(text("UPDATE flags SET status = :status, checksystem_response = :response WHERE flag = :flag"), {"status": FlagStatus.ACCEPTED.value if flag["status"] else FlagStatus.REJECTED.value, "flag": flag["flag"], "response": flag["msg"]})   
                connection.commit()
        except:
            pass