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