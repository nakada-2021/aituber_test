
from fastapi import FastAPI
from pydantic import BaseModel
import openai
import os
import uuid
from gtts import gTTS

app = FastAPI()
openai.api_key = os.getenv("OPENAI_API_KEY")

personas = {
    "default": "You are a helpful assistant.",
    "tsundere": "You are a tsundere character. Respond with a mix of rudeness and affection.",
    "kansai": "You are a Kansai dialect character. Speak casually in Kansai-ben.",
    "english_teacher": "You are an English teacher. Always respond in English."
}

class ChatInput(BaseModel):
    text: str
    persona: str = "default"
    lang: str = "ja"  # ja, en, zh

@app.post("/api/multilang_tts_chat")
def multilang_tts_chat(input: ChatInput):
    prompt = personas.get(input.persona, personas["default"])
    full_prompt = f"{prompt}\nUser:{input.text}\nAI:"

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": full_prompt}]
    )
    text_response = response["choices"][0]["message"]["content"]

    # 音声合成 (gTTS)
    tts = gTTS(text_response, lang=input.lang)
    audio_file = f"audio_{uuid.uuid4().hex}.mp3"
    tts.save(audio_file)

    return {
        "response": text_response,
        "audio_file": audio_file
    }
