import requests

API_URL = "http://127.0.0.1:8000/chat"

def chat_backend(message, disease):
    payload = {
        "message":message,
        "detected_disease": disease
    }
    res = requests.post(API_URL, json=payload)
    return res.json()["answer"]