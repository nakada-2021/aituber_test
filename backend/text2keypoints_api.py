
# backend/text2keypoints_api.py

from fastapi import FastAPI
from pydantic import BaseModel
import openai

app = FastAPI()

openai.api_key = "YOUR_API_KEY"  # 環境変数でも可

class TextInput(BaseModel):
    text: str

@app.post("/text2keypoints")
def text2keypoints(input: TextInput):
    prompt = f"""
以下の文章から感情を推定し、次の形式で出力してください（0〜1の範囲）:

{{
  "smile": (0-1),
  "sad": (0-1),
  "surprise": (0-1),
  "mouthOpen": (0-1)
}}

文章: {input.text}
"""

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "感情を推定して数値出力するAPIです。"},
            {"role": "user", "content": prompt}
        ]
    )

    import json
    return json.loads(response["choices"][0]["message"]["content"])
