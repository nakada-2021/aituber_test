
from fastapi import FastAPI, WebSocket
from pydantic import BaseModel
import openai
import os
from app import cloud_ws_tts_api

app = FastAPI()
openai.api_key = os.getenv("OPENAI_API_KEY")
app.mount("/ws", cloud_ws_tts_api.app)

class ChatInput(BaseModel):
    text: str

@app.post("/api/chat")
def chat(input: ChatInput):
    prompt = f"Q: {input.text}\nA:"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return {"response": response["choices"][0]["message"]["content"]}

@app.websocket("/api/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Echo: {data}")
