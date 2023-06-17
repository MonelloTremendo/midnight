import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

#from server.runner.runner import ExploitRunner

#ExploitRunner().update_list()

from routes.api import router as api_router
from routes.teams import router as teams_router
from routes.exploits import router as expl_router


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
app.include_router(teams_router)
app.include_router(expl_router)

#import server.routes.api

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)