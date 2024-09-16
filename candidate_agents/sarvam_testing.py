import requests

url = "https://api.sarvam.ai/translate"

headers = {
    'API-Subscription-Key': '',
}
data = {
    "input": "Hello, how are you today?",
    "source_language_code": "en-IN",
    "target_language_code": "ta-IN",
    "speaker_gender": "Male",
    "mode": "formal",
    "model": "mayura:v1",
    "enable_preprocessing": True
}

response = requests.post(url, headers=headers, json=data)
print(response.json())
