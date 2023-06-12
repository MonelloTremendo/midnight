import logging

from flask import Flask


app = Flask(__name__)

app.logger.setLevel(logging.DEBUG)
for handler in app.logger.handlers:
    handler.setLevel(logging.DEBUG)


import server.routes.api
import server.routes.views
import server.routes.teams
import server.routes.background
import server.routes.history
import server.routes.exploits
