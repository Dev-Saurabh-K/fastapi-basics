from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    # 1. Update broadcast to accept a Python dictionary (JSON)
    async def broadcast(self, data: dict):
        for connection in self.active_connections:
            await connection.send_json(data)

manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # 2. Receive structured data as a dictionary instead of a string
            data = await websocket.receive_json()
            
            # Extract incoming details sent by React
            username = data.get("username", "Anonymous")
            message_text = data.get("text", "")

            # 3. Construct a rich payload to send back to everyone
            payload = {
                "username": username,
                "text": message_text,
                "timestamp": time.strftime("%H:%M:%S") # Adds server-side timestamp
            }
            
            await manager.broadcast(payload)
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        # Broadcast a structured exit payload
        await manager.broadcast({
            "username": "System",
            "text": "An anonymous user left the chat.",
            "timestamp": time.strftime("%H:%M:%S")
        })