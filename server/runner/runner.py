#!/usr/bin/env python3

import sys

assert sys.version_info >= (3, 4), 'Python < 3.4 is not supported'

import argparse
import binascii
import itertools
import json
import logging
import os
import random
import re
import stat
import subprocess
import time
import threading
from concurrent.futures import ThreadPoolExecutor
from enum import Enum
from math import ceil
from urllib.parse import urljoin
from urllib.request import Request, urlopen


#log_format = '%(asctime)s {} %(message)s'.format(highlight('%(levelname)s', [Style.FG_YELLOW]))
#logging.basicConfig(format=log_format, datefmt='%H:%M:%S', level=logging.DEBUG)


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


#def get_config(args):
#    req = Request(urljoin(args.server_url, '/api/get_config'))
#    if args.token is not None:
#        req.add_header('X-Token', args.token)
#    with urlopen(req, timeout=SERVER_TIMEOUT) as conn:
#        if conn.status != 200:
#            raise APIException(conn.read())
#
#        return json.loads(conn.read().decode())
#
#
#def post_flags(args, flags):
#    sploit_name = os.path.basename(args.sploit)
#        
#    data = [{'flag': item['flag'], 'sploit': sploit_name, 'team': item['team']}
#            for item in flags]
#
#    req = Request(urljoin(args.server_url, '/api/post_flags'))
#    req.add_header('Content-Type', 'application/json')
#    if args.token is not None:
#        req.add_header('X-Token', args.token)
#    with urlopen(req, data=json.dumps(data).encode(), timeout=SERVER_TIMEOUT) as conn:
#        if conn.status != 200:
#            raise Exception(conn.read())

def once_in_a_period(period):
    for iter_no in itertools.count(1):
        start_time = time.time()
        yield iter_no

        time_spent = time.time() - start_time
        if period > time_spent:
            exit_event.wait(period - time_spent)
        if exit_event.is_set():
            break

#def run_post_loop(args):
#    try:
#        for _ in once_in_a_period(POST_PERIOD):
#            flags_to_post = flag_storage.pick_flags()
#
#            if flags_to_post:
#                try:
#                    post_flags(args, flags_to_post)
#
#                    flag_storage.mark_as_sent(len(flags_to_post))
#                    logging.info('{} flags posted to the server ({} in the queue)'.format(
#                        len(flags_to_post), flag_storage.queue_size))
#                except Exception as e:
#                    logging.error("Can't post flags to the server: {}".format(repr(e)))
#                    logging.info("The flags will be posted next time")
#    except Exception as e:
#        logging.critical('Posting loop died: {}'.format(repr(e)))
#        shutdown()


def process_sploit_output(stream, args, team_name, flag_format, attack_no):
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


def launch_sploit(args, team_name, team_addr, attack_no, flag_format):
    env = os.environ.copy()
    env['PYTHONUNBUFFERED'] = '1'

    command = [os.path.abspath(args.sploit)]
    command.append(team_addr)

    proc = subprocess.Popen(command,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            bufsize=1, close_fds=True, env=env)

    threading.Thread(target=lambda: process_sploit_output(
        proc.stdout, args, team_name, flag_format, attack_no)).start()

    return proc, instance_storage.register_start(proc)


def run_sploit(args, team_name, team_addr, attack_no, timeout, flag_format):
    try:
        with instance_lock:
            if exit_event.is_set():
                return

            proc, instance_id = launch_sploit(args, team_name, team_addr, attack_no, flag_format)
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

#def main(args):
#    threading.Thread(target=lambda: run_post_loop(args)).start()
#
#    pool = ThreadPoolExecutor(max_workers=args.pool_size)
#    for attack_no in once_in_a_period(args.attack_period):
#        for team_name, team_addr in teams.items():
#            pool.submit(run_sploit, args, team_name, team_addr, attack_no, max_runtime, flag_format)


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
