import uvicorn

from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware


from routes.teams import router as teams_router
from routes.exploits import router as expl_router, manager
from routes.stats import router as stats_router

from typing import List

import threading
from submit.submitter import submit_loop


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(teams_router)
app.include_router(expl_router)
app.include_router(stats_router)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            try:
                await websocket.receive()
            except:
                manager.disconnect(websocket)
                break        
    except:
        manager.disconnect(websocket)

threading.Thread(target=submit_loop).start()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)