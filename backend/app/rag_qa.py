
import requests
import os

LLM_URL = os.getenv("LLM_URL", "http://localhost:5000/completion")

def ask_local_llm(question):
    payload = {
        "prompt": question,
        "n_predict": 128,
        "temperature": 0.7
    }
    response = requests.post(LLM_URL, json=payload)
    return response.json()["content"]
