from fastapi import UploadFile, File, APIRouter
from fastapi.responses import JSONResponse
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

    matches_summary = "\n".join([
        (
            f"- {job['Job Title']} at {job['Company']} in {job['location']}, {job['Country']} "
            f"(Score: {round(job['match_score'], 2)})\n"
            f"  Work Type: {job['Work Type']}, Salary: {job['Salary Range']}, Role: {job['Role']}\n"
            f"  Skills: {job['skills']}\n"
            f"  Qualifications: {job['Qualifications']}\n"
            f"  Responsibilities: {job['Responsibilities'][:200]}..."
        )
        for job in results
    ])

    prompt = (
        f"You are an expert career coach and ATS (applicant tracking system) specialist.\n"
        f"Below is a candidate's resume:\n{resume_text}\n\n"
        f"The resume matched these jobs (including job titles, companies, locations, and key responsibilities/qualifications):\n{matches_summary}\n\n"
        f"Please provide a professional analysis:\n"
        f"1️⃣ Explain *why* this resume is a good match for these jobs, referring to specific parts of the resume and jobs.\n"
        f"2️⃣ Give 2-3 *specific* suggestions to improve the resume for these roles, focusing on content, structure, or keywords.\n"  
        f"Keep your tone clear and actionable.\n*END_OF_PROMPT*"
    )

    try:
        hf_model_reply = query_hf_model(prompt)
    except Exception as e:
        hf_model_reply = f"Error: {str(e)}"

    return JSONResponse({
        "uploaded_resume": resume.filename,
        "matches": results,
        "hf_model_reply": hf_model_reply
    })
