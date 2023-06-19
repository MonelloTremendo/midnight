from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

#    async def send_personal_message(self, message: str, websocket: WebSocket):
#        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

router = APIRouter(
    prefix="/ws",
    tags=["websocket"],
    responses={404: {"description": "Not found"}},
)

@router.websocket("/")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            try:
                await websocket.receive()
            except:
                manager.disconnect(websocket)
                break        
    except WebSocketDisconnect:
        manager.disconnect(websocket)