import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
headers = {"Authorization": f"Bearer {os.getenv('HUGGINGFACE_API_TOKEN')}"}

def query_mistral(prompt):
    payload = {
        "inputs": prompt,
        "parameters": {
            "temperature": 0.2,
            "max_new_tokens": 512
        }
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    response.raise_for_status()  # Will raise an error for 4xx/5xx codes
    return response.json()
