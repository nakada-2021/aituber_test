
from fastapi import FastAPI, WebSocket
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

app = FastAPI()
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

personas = {
    "default": "You are a helpful assistant.",
    "tsundere": "You are a tsundere character. Respond with a mix of rudeness and affection.",
    "kansai": "You are a Kansai dialect character. Speak casually in Kansai-ben.",
    "english_teacher": "You are an English teacher. Always respond in English."
}

class ChatInput(BaseModel):
    text: str
    persona: str = "default"
    lang: str = "ja"

@app.post("/api/cloud_tts_chat")
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

@app.get("/audio/{filename}")
def serve_audio(filename: str):
    file_path = f"/tmp/{filename}"
    return FileResponse(file_path, media_type="audio/mpeg")

# WebSocket音声ストリーム
@app.websocket("/ws/tts")
async def tts_ws(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        tts = gTTS(data, lang="ja")
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
        await websocket.send_json({"audio_url": audio_url})
