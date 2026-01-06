import requests

API_URL = "http://127.0.0.1:8000/detect"

def detect_disease(image_file):
    files = {"file":image_file}
    res = requests.post(
        API_URL,
        files=files
    )
    print(res)
    return res.json()