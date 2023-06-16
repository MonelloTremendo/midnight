from fastapi import FastAPI

#from server.runner.runner import ExploitRunner

#ExploitRunner().update_list()

from .routes.api import router as api_router
from .routes.teams import router as teams_router
from .routes.exploits import router as expl_router


app = FastAPI()

app.include_router(api_router)
app.include_router(teams_router)
app.include_router(expl_router)

#import server.routes.api