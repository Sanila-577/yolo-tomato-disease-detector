import requests

def chat_backend(message, disease):
    payload = {
        "message":message,
        "detected_disease": disease
    }
    res = requests.post(API_URL, json=payload)
    return res.json()["answer"]