
from fastapi import FastAPI
from pydantic import BaseModel
import openai
import os

app = FastAPI()
openai.api_key = os.getenv("OPENAI_API_KEY")

personas = {
    "default": "あなたは丁寧なAIアシスタントです。",
    "ツンデレ": "あなたはツンデレキャラクターです。ぶっきらぼうに返答してください。",
    "関西弁": "あなたは関西弁で話すキャラクターです。",
    "英語教師": "あなたは英語で返答する英語教師です。"
}

class PersonaInput(BaseModel):
    text: str
    persona: str = "default"
    lang: str = "ja"

@app.post("/api/persona_chat")
def persona_chat(input: PersonaInput):
    prompt = personas.get(input.persona, personas["default"])
    full_prompt = f"{prompt}\nユーザー:{input.text}\nAI:"
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": full_prompt}]
    )
    
    return {"response": response["choices"][0]["message"]["content"]}
