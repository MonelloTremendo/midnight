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

from server.database import database
from server.database import models
from server.config import config

def singleton(class_):
    instances = {}
    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance

@singleton
class ExploitRunner:
    def __init__(self) -> None:
        self.listLock = threading.RLock()
        self.exploits = {}
        self.instances = {}

        self.update_list()

    def update_list(self):
        result = database.query("SELECT * FROM exploits")

        with self.listLock:
            self.exploits = {item["id"] : {"name": item["name"], "threads": item["threads"], "timeout": item["timeout"], "source": item["source"], "running": int(item["running"]) == 1} for item in result}

            #to_delete = list(filter(lambda item: item not in self.exploits.keys(),self.instances.keys()))

            #for key in to_delete:
            #    self.instances[key].stop()
            #    del self.instances[key]

            for k,v in self.exploits.items():
                if v["running"]:
                    try:
                        if self.instances[k].source != v["source"]:
                            self.instances[k].stop()
                            del self.instances[k]

                            selectedTeams = database.query("SELECT * FROM exploit_teams INNER JOIN teams ON exploit_teams.team_id = teams.id WHERE exploit_teams.exploit_id = %s", (k,))
                            selectedTeams = [{"id": item["id"], "ip": item["ip"]} for item in selectedTeams]

                            self.instances[k] = Exploit(int(v["id"]), int(v["threads"]), int(v["timeout"]), v["source"], selectedTeams)
                            self.instances[k].run()
                    except KeyError:
                        selectedTeams = database.query("SELECT * FROM exploit_teams INNER JOIN teams ON exploit_teams.team_id = teams.id WHERE exploit_teams.exploit_id = %s", (k,))
                        selectedTeams = [{"id": item["id"], "ip": item["ip"]} for item in selectedTeams]

                        self.instances[k] = Exploit(k, int(v["threads"]), int(v["timeout"]), v["source"], selectedTeams)
                        self.instances[k].run()
                else:
                    try:
                        self.instances[k].stop()
                        del self.instances[k]
                    except KeyError:
                        pass
            print(self.instances)

    def delete_exploit(self, id):
        self.instances[id].stop()
        del self.instances[id]


class Exploit:
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
        self.path = os.path.abspath(os.path.join(config.get_config()["EXPLOIT_PATH"], filename))

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
        format = re.compile(config.get_config()["FLAG_FORMAT"])

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