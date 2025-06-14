import requests
import os
from dotenv import load_dotenv

load_dotenv()

HF_MODEL = os.getenv("HUGGINGFACE_MODEL")
HF_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")

print(f'MODEL FROM ENV: {HF_MODEL}')
print(f"TOKEN FROM ENV: {HF_TOKEN}")

def query_hf_model(prompt: str):
    url = f"https://api-inference.huggingface.co/models/{HF_MODEL}"
    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json"
    }
    
    formatted_prompt = f"<s>[INST] {prompt.strip()} [/INST]"
    
    payload = {
        "inputs": formatted_prompt,
        "parameters": {
            "temperature": 0.2,
            "max_new_tokens": 300
        }
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code != 200:
        raise Exception(f"Hugging Face API error: {response.status_code} - {response.text}")

    result = response.json()
    if isinstance(result, list) and "generated_text" in result[0]:
        return result[0]["generated_text"]
    else:
        raise Exception(f"Unexpected API response: {result}")