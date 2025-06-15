from fastapi import UploadFile, File, APIRouter
from fastapi.responses import JSONResponse
import numpy as np
from dotenv import load_dotenv
from ..resume_parser import extract_text_from_pdf
from ..job_matcher import match_jobs
from ..hf_model import query_hf_model

load_dotenv()

router = APIRouter()

@router.post("/match")
async def match_resume(resume: UploadFile = File(...)):
    content = await resume.read()
    
    resume_text = extract_text_from_pdf(content)
    if not resume_text:
        return JSONResponse({"error":"Could not extract text from resume."}, status_code=400)

    results = match_jobs(resume_text)

    matches_summary = "\n".join(
        [f"- {job['title']} at {job['company']} in {job['location']} (Score: {round(job['match_score'], 2)})" for job in results]
    )
    prompt = (
        f"I have a resume that matched the following jobs:\n{matches_summary}\n\n"
        f"Please provide a short analysis:\n"
        f"1. Why do these jobs match the resume?\n"
        f"2. What are 2-3 suggestions to improve the resume for these roles?\n"
    )

    try:
        hf_model_reply = query_hf_model("Tell me a fun fact about sweden.")
        # hf_model_reply = query_hf_model(prompt)
    except Exception as e:
        hf_model_reply = f"Error: {str(e)}"

    return JSONResponse({
        "uploaded_resume": resume.filename,
        "matches": results,
        "hf_model_reply": hf_model_reply
    })
