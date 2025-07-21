
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
import openai
import os
import uuid
from gtts import gTTS
import shutil
from fastapi.responses import FileResponse
try:
    import boto3
except ImportError:
    boto3 = None

# WebSocket接続管理
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        print(f"WebSocket connected. Total connections: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        print(f"WebSocket disconnected. Total connections: {len(self.active_connections)}")

    async def broadcast(self, message: dict):
        """すべての接続中のクライアントにメッセージを送信"""
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                print(f"Failed to send message to client: {e}")
                disconnected.append(connection)
        
        # 切断された接続を削除
        for connection in disconnected:
            self.disconnect(connection)

manager = ConnectionManager()

# app = FastAPI() ← 削除
openai.api_key = os.getenv("OPENAI_API_KEY")

# GCP設定
GCS_BUCKET = os.getenv("GCS_BUCKET")
GCS_URL_PREFIX = os.getenv("GCS_URL_PREFIX", "https://storage.googleapis.com")

# S3設定
AUDIO_STORAGE = os.getenv("AUDIO_STORAGE", "local")
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

# ペルソナ設定
personas = {
    "default": "You are a helpful assistant. Respond in Japanese.",
    "tsundere": "You are a tsundere character. Respond with a mix of rudeness and affection in Japanese.",
    "kansai": "You are a Kansai dialect character. Speak casually in Kansai-ben.",
    "english_teacher": "You are an English teacher. Always respond in English."
}

class ChatInput(BaseModel):
    text: str
    persona: str = "default"
    lang: str = "ja"

def cloud_tts_chat(input: ChatInput):
    prompt = personas.get(input.persona, personas["default"])
    full_prompt = f"{prompt}\nUser:{input.text}\nAI:"

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": full_prompt}]
    )
    text_response = response["choices"][0]["message"]["content"]

    # 音声合成 (gTTS)
    tts = gTTS(text_response, lang=input.lang)
    filename = f"audio_{uuid.uuid4().hex}.mp3"
    local_file = f"/tmp/{filename}"
    tts.save(local_file)

    if AUDIO_STORAGE == "gcs":
        blob = bucket.blob(filename)
        blob.upload_from_filename(local_file)
        audio_url = f"{GCS_URL_PREFIX}/{GCS_BUCKET}/{filename}"
    elif AUDIO_STORAGE == "s3":
        if boto3 is None:
            raise RuntimeError("boto3 is not installed")
        s3 = boto3.client(
            "s3",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=AWS_S3_REGION
        )
        s3.upload_file(local_file, AWS_S3_BUCKET, filename, ExtraArgs={"ContentType": "audio/mpeg"})
        audio_url = f"{AWS_S3_URL_PREFIX}/{filename}"
    else:
        # local
        audio_url = f"/audio/{filename}"
        # /tmpに保存済み
    return {
        "response": text_response,
        "audio_url": audio_url
    }

def serve_audio(filename: str):
    file_path = f"/tmp/{filename}"
    return FileResponse(file_path, media_type="audio/mpeg")

# WebSocket音声ストリーム（ブロードキャスト対応）
async def tts_ws(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Received text from client: {data}")
            
            # AIレスポンスを生成
            prompt = personas.get("default", personas["default"])
            full_prompt = f"{prompt}\nUser:{data}\nAI:"
            
            print(f"Generating AI response...")
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": full_prompt}]
            )
            text_response = response["choices"][0]["message"]["content"]
            print(f"AI response: {text_response}")
            
            # AIレスポンスを音声合成
            print(f"Generating audio...")
            tts = gTTS(text_response, lang="ja")
            filename = f"audio_{uuid.uuid4().hex}.mp3"
            local_file = f"/tmp/{filename}"
            tts.save(local_file)
            
            if AUDIO_STORAGE == "gcs":
                blob = bucket.blob(filename)
                blob.upload_from_filename(local_file)
                audio_url = f"{GCS_URL_PREFIX}/{GCS_BUCKET}/{filename}"
            elif AUDIO_STORAGE == "s3":
                if boto3 is None:
                    raise RuntimeError("boto3 is not installed")
                s3 = boto3.client(
                    "s3",
                    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
                    region_name=AWS_S3_REGION
                )
                s3.upload_file(local_file, AWS_S3_BUCKET, filename, ExtraArgs={"ContentType": "audio/mpeg"})
                audio_url = f"{AWS_S3_URL_PREFIX}/{filename}"
            else:
                audio_url = f"/audio/{filename}"
            
            # すべての接続中のクライアントにブロードキャスト
            response_data = {
                "response": text_response,
                "audio_url": audio_url,
                "source": "broadcast"
            }
            print(f"Broadcasting response to {len(manager.active_connections)} clients: {response_data}")
            await manager.broadcast(response_data)
            print(f"Broadcast completed successfully")
            
    except WebSocketDisconnect:
        # クライアントが正常に切断した場合
        print("WebSocket client disconnected normally")
        manager.disconnect(websocket)
    except Exception as e:
        # その他のエラー
        print(f"WebSocket error: {e}")
        manager.disconnect(websocket)
        raise
