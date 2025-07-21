
from fastapi import FastAPI, WebSocket
from pydantic import BaseModel
import openai
import os
from app import cloud_ws_tts_api
import uuid
from gtts import gTTS
import shutil
from fastapi.responses import FileResponse
try:
    import boto3
except ImportError:
    boto3 = None

app = FastAPI()
openai.api_key = os.getenv("OPENAI_API_KEY")

AUDIO_STORAGE = os.getenv("AUDIO_STORAGE", "local")
GCS_BUCKET = os.getenv("GCS_BUCKET")
GCS_URL_PREFIX = os.getenv("GCS_URL_PREFIX", "https://storage.googleapis.com")
AWS_S3_BUCKET = os.getenv("AWS_S3_BUCKET")
AWS_S3_REGION = os.getenv("AWS_S3_REGION", "ap-northeast-1")
AWS_S3_URL_PREFIX = os.getenv("AWS_S3_URL_PREFIX", f"https://{AWS_S3_BUCKET}.s3.amazonaws.com")
if AUDIO_STORAGE == "gcs":
    from google.cloud import storage
    storage_client = storage.Client()
    bucket = storage_client.bucket(GCS_BUCKET)
else:
    storage_client = None
    bucket = None

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

# cloud_ws_tts_api.pyのAPIエンドポイントをmain.pyに統合
app.post("/api/cloud_tts_chat")(cloud_ws_tts_api.cloud_tts_chat)
app.get("/audio/{filename}")(cloud_ws_tts_api.serve_audio)
app.websocket("/ws/tts")(cloud_ws_tts_api.tts_ws)
