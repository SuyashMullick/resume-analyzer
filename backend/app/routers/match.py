from fastapi import UploadFile, File, APIRouter
from fastapi.responses import JSONResponse
import numpy as np
from dotenv import load_dotenv
from ..hf_model import query_hf_model

load_dotenv()

router = APIRouter()

# Dummy job metadata
metadata = [
    {"title": "Software Engineer", "company": "Acme Inc"},
    {"title": "Data Scientist", "company": "Beta AI"},
    {"title": "ML Engineer", "company": "Gamma Tech"},
]

def search_jobs_vector(resume_content):
    indices = np.array([[0, 1, 2]])
    distances = np.array([[5.0, 10.0, 20.0]])
    return indices, distances

@router.post("/match")
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
        mistral_reply = query_hf_model("Tell me a fun fact about sweden.")
        # mistral_reply = query_hf_model(prompt)
    except Exception as e:
        mistral_reply = f"Error: {str(e)}"

    return JSONResponse({
        "uploaded_resume": resume.filename,
        "matches": results,
        "mistral_reply": mistral_reply
    })
