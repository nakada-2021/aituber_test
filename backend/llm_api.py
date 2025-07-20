
# backend/llm_api.py

from fastapi import FastAPI, WebSocket
import openai
import asyncio

app = FastAPI()

openai.api_key = "YOUR_API_KEY"

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        print("Received:", data)
        # ここでLLM呼び出し可
