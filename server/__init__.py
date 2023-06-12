import logging

from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/":{'origins':''}})

app.logger.setLevel(logging.DEBUG)
for handler in app.logger.handlers:
    handler.setLevel(logging.DEBUG)

import server.routes.api
import server.routes.views
import server.routes.teams
import server.routes.background
import server.routes.history
import server.routes.exploits
