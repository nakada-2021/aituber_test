
from fastapi import FastAPI, WebSocket
from pydantic import BaseModel
import openai
import os
import uuid
from gtts import gTTS
from google.cloud import storage

app = FastAPI()
openai.api_key = os.getenv("OPENAI_API_KEY")

# GCP設定
GCS_BUCKET = os.getenv("GCS_BUCKET")
GCS_URL_PREFIX = os.getenv("GCS_URL_PREFIX", "https://storage.googleapis.com")

storage_client = storage.Client()
bucket = storage_client.bucket(GCS_BUCKET)

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

    # GCSアップロード
    blob = bucket.blob(filename)
    blob.upload_from_filename(local_file)
    audio_url = f"{GCS_URL_PREFIX}/{GCS_BUCKET}/{filename}"

    return {
        "response": text_response,
        "audio_url": audio_url
    }

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

        # GCSアップロード
        blob = bucket.blob(filename)
        blob.upload_from_filename(local_file)
        audio_url = f"{GCS_URL_PREFIX}/{GCS_BUCKET}/{filename}"

        await websocket.send_json({"audio_url": audio_url})
