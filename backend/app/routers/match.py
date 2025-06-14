from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import os
import requests
import numpy as np
from dotenv import load_dotenv

# Load .env
load_dotenv()

HF_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")
HF_MODEL = "mistralai/Mistral-7B-Instruct-v0.2"

app = FastAPI()

# Dummy job metadata
metadata = [
    {"title": "Software Engineer", "company": "Acme Inc"},
    {"title": "Data Scientist", "company": "Beta AI"},
    {"title": "ML Engineer", "company": "Gamma Tech"},
    # More jobs...
]

def search_jobs_vector(resume_content):
    indices = np.array([[0, 1, 2]])
    distances = np.array([[5.0, 10.0, 20.0]])
    return indices, distances

def query_mistral(prompt: str):
    url = f"https://api-inference.huggingface.co/models/{HF_MODEL}"
    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "inputs": prompt,
        "parameters": {
            "temperature": 0.2,
            "max_new_tokens": 300
        }
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code != 200:
        raise Exception(f"Hugging Face API error: {response.status_code} - {response.text}")
    # The API returns a list of dicts with 'generated_text'
    result = response.json()
    return result[0]["generated_text"]

@app.post("/match")
async def match_resume(resume: UploadFile = File(...)):
    content = await resume.read()
    
    indices, distances = search_jobs_vector(content)

    results = []
    for idx, dist in zip(indices[0], distances[0]):
        job = metadata[idx].copy()
        job["relevance_score"] = round(100 - dist, 2)
        results.append(job)

    matches_summary = "\n".join(
        [f"- {job['title']} at {job['company']} (Relevance: {job['relevance_score']}%)" for job in results]
    )
    prompt = (
        f"I have a resume that matched the following jobs:\n{matches_summary}\n\n"
        f"Please provide a short analysis:\n"
        f"1. Why do these jobs match the resume?\n"
        f"2. What are 2-3 suggestions to improve the resume for these roles?\n"
    )

    try:
        mistral_reply = query_mistral(prompt)
    except Exception as e:
        mistral_reply = f"Error: {str(e)}"

    return JSONResponse({
        "uploaded_resume": resume.filename,
        "matches": results,
        "mistral_reply": mistral_reply
    })
