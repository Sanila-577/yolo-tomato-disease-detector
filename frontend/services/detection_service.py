import requests

def detect_disease(image_file):
    files = {"file":image_file}
    res = requests.post(
        API_URL,
        files=files
    )
    return res.json()