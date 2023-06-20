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
        flags = connection.execute(text("SELECT * FROM flags WHERE status = 0 LIMIT 500")).fetchall()
        flags = [Flag.from_orm(flag) for flag in flags]

        try:
            #response = requests.put(config['CHECKSYSTEM_URL'], headers={'X-Team-Token': config['CHECKSYSTEM_TOKEN']}, json=[item.flag for item in flags], timeout=5)

            for flag in flags:
                connection.execute(text("UPDATE flags SET status = :status WHERE flag = :flag"), {"status": random.randint(1, 2), "flag": flag.flag})

            connection.commit()
            time.sleep(1)
        except:
            pass