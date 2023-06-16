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

from fastapi import  Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from ..database.connection import get_db
from ..database.models import Exploit, Team

from ..config.config import get_config

lock = threading.RLock()
instances = {}

def init():
    pass

def run_exploit(id: int):
    conn = next(get_db())
    exploit = conn.execute(text("SELECT * FROM exploits WHERE id = :exploit_id"), { "exploit_id" : id }).fetchone()
    exploit = Exploit.from_orm(exploit)

    teams = conn.execute(text("SELECT teams.id, teams.name, teams.ip FROM exploit_teams INNER JOIN teams ON exploit_teams.team_id = teams.id WHERE exploit_teams.exploit_id = :exploit_id"), { "exploit_id" : id }).fetchall()
    teams = [Team.from_orm(team) for team in teams]

    print(exploit)
    print(teams)

def stop_exploit(id: int, db: Session = Depends(get_db)):
    pass

def update_exploit(id: int, db: Session = Depends(get_db)):
    pass

#def update_list(self):
#    connection = next(get_db())
#
#    result = connection.execute("SELECT * FROM exploits")
#
#    with lock:
#        exploits = {item["id"] : {"name": item["name"], "threads": item["threads"], "timeout": item["timeout"], "source": item["source"], "running": int(item["running"]) == 1} for item in result}
#
#        for k,v in exploits.items():
#            if v["running"]:
#                try:
#                    if instances[k].source != v["source"]:
#                        instances[k].stop()
#                        del instances[k]
#
#                        selectedTeams = database.query("SELECT * FROM exploit_teams INNER JOIN teams ON exploit_teams.team_id = teams.id WHERE exploit_teams.exploit_id = %s", (k,))
#                        selectedTeams = [{"id": item["id"], "ip": item["ip"]} for item in selectedTeams]
#
#                        instances[k] = Exploit(int(v["id"]), int(v["threads"]), int(v["timeout"]), v["source"], selectedTeams)
#                        instances[k].run()
#                except KeyError:
#                    selectedTeams = database.query("SELECT * FROM exploit_teams INNER JOIN teams ON exploit_teams.team_id = teams.id WHERE exploit_teams.exploit_id = %s", (k,))
#                    selectedTeams = [{"id": item["id"], "ip": item["ip"]} for item in selectedTeams]
#
#                    instances[k] = Exploit(k, int(v["threads"]), int(v["timeout"]), v["source"], selectedTeams)
#                    instances[k].run()
#            else:
#                try:
#                    instances[k].stop()
#                    del instances[k]
#                except KeyError:
#                    pass
#        print(instances)

#def delete_exploit(self, id):
#    self.instances[id].stop()
#    del self.instances[id]
    


class ExploitRunner:
    def __init__(self, id, threads, timeout, source, targets) -> None:
        self.lock = threading.RLock()
        self.exit_event = threading.Event()
        self.pool = ThreadPoolExecutor(max_workers=threads)
        self.id = id
        self.timeout = timeout
        self.targets = targets
        self.source = source

        self.period = 30

        self.instance_counter = 0
        self.instances = {}

        filename = "".join(random.choice(string.ascii_letters + string.digits) for _ in range(10))
        self.path = os.path.abspath(os.path.join(get_config()["EXPLOIT_PATH"], filename))

        with open(self.path, "w") as f:
            f.write(source)
        
        file_mode = os.stat(self.path).st_mode
        os.chmod(self.path, file_mode | stat.S_IXUSR)

    def once_in_a_period(self, period):
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
        for _ in self.once_in_a_period(self.period):
            for item in self.targets:
                with self.lock:
                    if self.exit_event.is_set():
                        return
                self.pool.submit(self.start_exploit, item)

    def stop(self):
        self.exit_event.set()

        with self.lock:
            for proc in self.instances:
                proc.kill()

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

    def start_exploit(self, target):
        with self.lock:
            if self.exit_event.is_set():
                return

        flag_storage = set()
        env = os.environ.copy()
        env['PYTHONUNBUFFERED'] = '1'

        command = [self.path]
        command.append(target["ip"])

        proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1, close_fds=True, env=env)
        process_thread = threading.Thread(target=lambda: self.flag_processor(proc.stdout, flag_storage))
        process_thread.start()
        
        with self.lock:
            instance_id = self.instance_counter
            self.instance_counter += 1
            self.instances[instance_id] = proc
            #print(self.instances)

        try:
            proc.wait(timeout=self.timeout)
            need_kill = False
        except subprocess.TimeoutExpired:
            need_kill = True

        with self.lock:
            if need_kill:
                proc.kill()

            del self.instances[instance_id]

        process_thread.join()

        with self.lock:
            if self.exit_event.is_set():
                return
        
        exec_time = int(time.time())

        conn = database.get()
        cursor = conn.cursor(dictionary=True, buffered=True)

        cursor.execute("INSERT INTO runs (exploit_id, team_id, time) VALUES (%s, %s, %s)", (self.id, target["id"], exec_time))
        run_id = cursor.lastrowid

        rows = [(flag, run_id, models.FlagStatus.QUEUED.value, None) for flag in flag_storage]
        cursor.executemany("INSERT IGNORE INTO flags VALUES (%s, %s, %s, %s)", rows)

        conn.commit()

    def __del__(self):
        self.stop()