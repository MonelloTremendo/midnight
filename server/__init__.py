import logging
import multiprocessing

from flask import Flask
from flask_cors import CORS

from server.runner.runner import ExploitRunner

#multiprocessing.set_start_method('spawn')

app = Flask(__name__)
CORS(app, resources={r"/":{'origins':''}})

app.logger.setLevel(logging.DEBUG)
for handler in app.logger.handlers:
    handler.setLevel(logging.DEBUG)

ExploitRunner().update_list()

import server.routes.api
import server.routes.views
import server.routes.teams
import server.routes.background
import server.routes.history
import server.routes.exploits
