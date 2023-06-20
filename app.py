import uvicorn

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from routes.websocket import router as ws_router
from routes.api import router as api_router
from routes.teams import router as teams_router
from routes.exploits import router as expl_router
from routes.stats import router as stats_router

import threading
from submit.submit_loop import submit_loop

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
app.include_router(stats_router)
app.include_router(ws_router)

threading.Thread(target=submit_loop).start()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)