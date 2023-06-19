import itertools
import logging
import os
import re
import subprocess
import time
import threading
import random
import string
import stat
from concurrent.futures import ThreadPoolExecutor

from typing import List

from fastapi import  Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from database.connection import get_db
from database.models import Exploit, Team, Flag, FlagStatus

from config.config import get_config

import base64

lock = threading.RLock()
instances = dict()

def run_exploit(id: int):
    conn = next(get_db())
    exploit = conn.execute(text("SELECT * FROM exploits WHERE id = :exploit_id"), { "exploit_id" : id }).fetchone()
    exploit = Exploit.from_orm(exploit)

    teams = conn.execute(text("SELECT teams.id, teams.name, teams.ip FROM exploit_teams INNER JOIN teams ON exploit_teams.team_id = teams.id WHERE exploit_teams.exploit_id = :exploit_id"), { "exploit_id" : id }).fetchall()
    teams = [Team.from_orm(team) for team in teams]

    with lock:
        if id not in instances:
            instances[id] = ExploitRunner(exploit, teams)
            instances[id].run()
            return True
        else:
            return False

def stop_exploit(id: int):
    with lock:
        if id in instances:
            instances[id].stop()
            del instances[id]
            return True
        else:
            return False

def update_exploit(id: int):
    if is_running(id):
        stop_exploit(id)
        run_exploit(id)

def is_running(id: int):
    with lock:
        return id in instances


class ExploitRunner:
    def __init__(self, exploit: Exploit, targets: List[Team]) -> None:
        self.lock = threading.RLock()
        self.exit_event = threading.Event()
        self.pool = ThreadPoolExecutor(max_workers=exploit.threads)

        self.exploit = exploit
        self.targets = targets

        self.instance_counter = 0
        self.instances = {}

        filename = "".join(random.choice(string.ascii_letters + string.digits) for _ in range(10))
        self.path = os.path.abspath(os.path.join(get_config()["EXPLOIT_PATH"], filename))

        with open(self.path, "wb") as f:
            decoded = base64.b64decode(exploit.source)
            f.write(decoded)
        
        file_mode = os.stat(self.path).st_mode
        os.chmod(self.path, file_mode | stat.S_IXUSR)

    def once_in_a_period(self, period) -> int:
        for iter_no in itertools.count(1):
            start_time = time.time()
            yield iter_no

            time_spent = time.time() - start_time
            if period > time_spent:
                self.exit_event.wait(period - time_spent)
            if self.exit_event.is_set():
                break

    def run(self):
        threading.Thread(target=self.run_loop).start()

    def run_loop(self):
        for _ in self.once_in_a_period(self.exploit.runperiod):
            for item in self.targets:
                if self.exit_event.is_set():
                    return
                self.pool.submit(self.start_exploit, item)

    def stop(self):
        self.exit_event.set()

        with self.lock:
            for proc in self.instances:
                self.instances[proc].kill()

    def flag_processor(self, stream, store):
        format = re.compile(get_config()["FLAG_FORMAT"])

        try:
            while True:
                line = stream.readline()
                if not line or self.exit_event.is_set():
                    break
                line = line.decode(errors='replace')

                line_flags = set(format.findall(line))
                if line_flags:
                    store |= line_flags

        except Exception as e:
            logging.error('Failed to process sploit output: {}'.format(repr(e)))

    def start_exploit(self, target: Team):
        if self.exit_event.is_set():
            return

        flag_storage = set()
        env = os.environ.copy()
        env['PYTHONUNBUFFERED'] = '1'

        command = [self.path]
        command.append(target.ip)

        start_time = int(time.time())

        proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1, close_fds=True, env=env)
        process_thread = threading.Thread(target=lambda: self.flag_processor(proc.stdout, flag_storage))
        process_thread.start()
        
        with self.lock:
            instance_id = self.instance_counter
            self.instance_counter += 1
            self.instances[instance_id] = proc

        try:
            proc.wait(timeout=self.exploit.timeout)
        except subprocess.TimeoutExpired:
            proc.kill()

        with self.lock:
            del self.instances[instance_id]

        process_thread.join()

        if self.exit_event.is_set():
            return
        
        end_time = int(time.time())

        db = next(get_db())
        result = db.execute(text("INSERT INTO runs (exploit_id, team_id, start_time, end_time, exitcode) VALUES (:exploit_id, :team_id, :start_time, :end_time, :exitcode)"), { "exploit_id": self.exploit.id, "team_id": target.id, "start_time": start_time, "end_time": end_time, "exitcode": proc.returncode })

        for flag in flag_storage:
            db.execute(text("INSERT IGNORE INTO flags VALUES (:flag, :run_id, :status, :checksystem_response)"), Flag(flag=flag, run_id=result.lastrowid).dict())

        db.commit()

    def __del__(self):
        self.stop()