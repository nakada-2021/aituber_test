
import os
import requests
import openai

LOCAL_LLM = os.getenv("LOCAL_LLM", "on")
LLM_URL = os.getenv("LLM_URL", "http://localhost:5000/completion")

def ask_question(question):
    if LOCAL_LLM == "on":
        try:
            payload = {
                "prompt": question,
                "n_predict": 128,
                "temperature": 0.7
            }
            response = requests.post(LLM_URL, json=payload, timeout=5)
            return response.json().get("content", "")
        except Exception as e:
            print(f"ローカルLLM失敗: {e}")
            # フォールバック
            return ask_openai(question)
    else:
        return ask_openai(question)

def ask_openai(question):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": question}]
    )
    return completion.choices[0].message.content


