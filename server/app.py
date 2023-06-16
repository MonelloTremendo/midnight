from fastapi import FastAPI

#from server.runner.runner import ExploitRunner

app = FastAPI()

#ExploitRunner().update_list()

import server.routes.api
import server.routes.teams
#import server.routes.background
#import server.routes.history
#import server.routes.exploits
