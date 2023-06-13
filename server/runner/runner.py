import itertools
import logging
import os
import re
import subprocess
import time
import threading
from concurrent.futures import ThreadPoolExecutor

from server.database import database

MAX_WORKERS = 16

def singleton(class_):
    instances = {}
    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance

def once_in_a_period(period):
    for iter_no in itertools.count(1):
        start_time = time.time()
        yield iter_no

        time_spent = time.time() - start_time
        if period > time_spent:
            exit_event.wait(period - time_spent)
        if exit_event.is_set():
            break

@singleton
class ExploitRunner:
    def __init__(self) -> None:
        self.pool = ThreadPoolExecutor(max_workers=MAX_WORKERS)
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

class Exploit:
    def __init__(self, ) -> None:
        self.lock = threading.RLock()
#        self.process


#                    env = os.environ.copy()
#            env['PYTHONUNBUFFERED'] = '1'
#
#            command = [os.path.abspath(args.sploit)]
#            command.append(team_addr)
#
#            proc = subprocess.Popen(command,
#                                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
#                                    bufsize=1, close_fds=True, env=env)
#
#            threading.Thread(target=lambda: process_sploit_output(
#                proc.stdout, args, team_name, flag_format, attack_no)).start()

    def flag_processor(self):
        pass

    def start(self):
        pass

    def kill(self):
        with self.lock:
            pass
    pass

class FlagStorage:
    """
    Thread-safe storage comprised of a set and a post queue.

    Any number of threads may call add(), but only one "consumer thread"
    may call pick_flags() and mark_as_sent().
    """

    def __init__(self):
        self._flags_seen = set()
        self._queue = []
        self._lock = threading.RLock()

    def add(self, flags, team_name):
        with self._lock:
            for item in flags:
                if item not in self._flags_seen:
                    self._flags_seen.add(item)
                    self._queue.append({'flag': item, 'team': team_name})

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

class InstanceStorage:
    """
    Storage comprised of a dictionary of all running sploit instances and some statistics.

    Always acquire instance_lock before using this class. Do not release the lock
    between actual spawning/killing a process and calling register_start()/register_stop().
    """

    def __init__(self):
        self._counter = 0
        self.instances = {}

        self.n_completed = 0
        self.n_killed = 0

    def register_start(self, process):
        instance_id = self._counter
        self.instances[instance_id] = process
        self._counter += 1
        return instance_id

    def register_stop(self, instance_id, was_killed):
        del self.instances[instance_id]

        self.n_completed += 1
        self.n_killed += was_killed


exit_event = threading.Event()

flag_storage = FlagStorage()
instance_storage = InstanceStorage()
instance_lock = threading.RLock()

POST_PERIOD = 5
SERVER_TIMEOUT = 5

def process_sploit_output(stream, team_name, flag_format):
    try:
        output_lines = []
        instance_flags = set()

        while True:
            line = stream.readline()
            if not line:
                break
            line = line.decode(errors='replace')
            output_lines.append(line)

            line_flags = set(flag_format.findall(line))
            if line_flags:
                flag_storage.add(line_flags, team_name)
                instance_flags |= line_flags
    except Exception as e:
        logging.error('Failed to process sploit output: {}'.format(repr(e)))


def run_sploit(args, team_name, team_addr, attack_no, timeout, flag_format):
    try:
        with instance_lock:
            if exit_event.is_set():
                return

            proc, instance_id = launch_sploit(args, team_name, team_addr, attack_no, flag_format)

            env = os.environ.copy()
            env['PYTHONUNBUFFERED'] = '1'

            command = [os.path.abspath(args.sploit)]
            command.append(team_addr)

            proc = subprocess.Popen(command,
                                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                    bufsize=1, close_fds=True, env=env)

            threading.Thread(target=lambda: process_sploit_output(
                proc.stdout, args, team_name, flag_format, attack_no)).start()

            #return proc, instance_storage.register_start(proc)
    except Exception as e:
        return

    try:
        try:
            proc.wait(timeout=timeout)
            need_kill = False
        except subprocess.TimeoutExpired:
            need_kill = True

        with instance_lock:
            if need_kill:
                proc.kill()

            instance_storage.register_stop(instance_id, need_kill)
    except Exception as e:
        pass

def main(args):
    #threading.Thread(target=lambda: run_post_loop(args)).start()

    pool = ThreadPoolExecutor(max_workers=MAX_WORKERS)
    for attack_no in once_in_a_period(args.attack_period):
        for team_name, team_addr in teams.items():
            pool.submit(run_sploit, args, team_name, team_addr, attack_no, max_runtime, flag_format)


#def shutdown():
#    # Stop run_post_loop thread
#    exit_event.set()
#    # Kill all child processes (so consume_sploit_ouput and run_sploit also will stop)
#    with instance_lock:
#        for proc in instance_storage.instances.values():
#            proc.kill()


#if __name__ == '__main__':
#    try:
#        main()
#    except KeyboardInterrupt:
#        logging.info('Got Ctrl+C, shutting down')
#    finally:
#        shutdown()
