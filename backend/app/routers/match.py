from fastapi import APIRouter, UploadFile, File
import faiss
import numpy as np
import pickle
from app.embeddings import embed_text
from PyPDF2 import PdfReader

router = APIRouter()

# Load index + metadata once
index = faiss.read_index("backend/data/faiss_jobs.index")
with open("backend/data/job_metadata.pkl", "rb") as f:
    metadata = pickle.load(f)

@router.post("/match")
async def search_jobs(resume: UploadFile = File(...)):
    pdf = PdfReader(resume.file)
    text = "\n".join(page.extract_text() or "" for page in pdf.pages)

    embedding = embed_text(text)
    embedding_vector = np.array([embedding], dtype="float32")

    k = 3
    distances, indices = index.search(embedding_vector, k)

    results = []
    for idx, dist in zip(indices[0], distances[0]):
        job = metadata[idx]
        job["relevance_score"] = round(100 - dist, 2)
        results.append(job)

    return {
        "uploaded_resume": resume.filename,
        "matches": results
    }
