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

        self.update_list()

    def update_list(self):
        result = database.query("SELECT * FROM exploits")

        with self.listLock:
            self.exploits = {item["id"] : {"name": item["name"], "threads": item["threads"], "timeout": item["timeout"], "source": item["source"], "running": item["running"] == 1} for item in result}

    def print_list(self):
        self.update_list()

        print(self.exploits)

    def execute_scripts(self):
        for k, v in self.exploits.items():
            print(k, v)

class FlagStorage:
    def __init__(self):
        self._flags_seen = set()
        self._queue = []
        self._lock = threading.RLock()

    def add(self, flags):
        with self._lock:
            for item in flags:
                if item not in self._flags_seen:
                    self._flags_seen.add(item)
                    self._queue.append(item)

    def pick_flags(self):
        with self._lock:
            return self._queue[:]

    def mark_as_sent(self, count):
        with self._lock:
            self._queue = self._queue[count:]

    @property
    def queue_size(self):
        with self._lock:
            return len(self._queue)


class Exploit:
    def __init__(self, id, threads, timeout, source, targets) -> None:
        self.lock = threading.RLock()
        self.exit_event = threading.Event()
        self.pool = ThreadPoolExecutor(max_workers=threads)
        self.running = False
        self.id = id
        self.timeout = timeout
        self.targets = targets

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
        for _ in self.once_in_a_period():
            for item in self.targets.items():
                self.pool.submit(self.start_exploit, item)

    def stop(self):
        self.exit_event.set()

        with self.instance_lock:
            for proc in self.instance_storage:
                proc.kill()
        pass

    def flag_processor(self, stream, store):
        format = config.get_config()["FLAG_FORMAT"]

        try:
            while True:
                line = stream.readline()
                if not line:
                    break
                line = line.decode(errors='replace')

                line_flags = set(format.findall(line))
                if line_flags:
                    store |= line_flags

        except Exception as e:
            logging.error('Failed to process sploit output: {}'.format(repr(e)))

    def start_exploit(self, target):
        with self.instance_lock:
            if self.exit_event.is_set():
                return

        flag_storage = set()
        env = os.environ.copy()
        env['PYTHONUNBUFFERED'] = '1'

        command = [self.path]
        command.append(target.ip)

        proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1, close_fds=True, env=env)
        process_thread = threading.Thread(target=lambda: self.flag_processor(proc.stdout, flag_storage))
        
        with self.lock:
            instance_id = self.instance_counter
            self.instances[instance_id] = proc

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
        exec_time = time.time_ns() // 1_000_000

        conn = database.get()
        cursor = conn.cursor()

        cursor.execute("INSERT INTO runs (exploit_id, team_id, time) VALUES (?, ?, ?)", (self.id, target.id, exec_time))
        run_id = cursor.lastrowid

        rows = [(flag, run_id, models.FlagStatus.QUEUED, None) for flag in flag_storage]
        cursor.executemany("INSERT INTO flags VALUES (?, ?, ?, ?)", rows)

        conn.commit()

    def __del__(self):
        self.stop()