from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import time


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()

        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, data:dict):
        for connection in self.active_connections:
            await connection.send_text(data)

manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    #Accept and track the new connection
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()

            username = data.get("username", "Anonymous")
            message_text = data.get("text", "")

            payload = {
                "username": username,
                "text": message_text,
                "timestamp": time.strftime("%H:%M:%S")
            }
            await manager.broadcast(payload)

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast({
            "username": "System",
            "text": "An anonymous user left the chat.",
            "timestamp": time.strftime("%H:%M:%S")
        })
    # await websocket.accept()
    # try:
    #     while True:
    #         data = await websocket.receive_text()
    #         print(data)
    #         await websocket.send_text(f"Message recieved: {data}")
    # except WebSocketDisconnect:
    #     print("Client disconnected gracefully.")
        