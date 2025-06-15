import faiss
import numpy as np
import pickle
from .embeddings import embed_text

index = faiss.read_index("backend/data/faiss_jobs.index")
with open("backend/data/job_metadata.pkl", "rb") as f:
    metadata = pickle.load(f)

def match_jobs(resume_text: str, top_k: int = 3):
    vector = np.array([embed_text(resume_text)], dtype="float32")
    scores, indices = index.search(vector, top_k)
    
    results = []
    for idx, score in zip(indices[0], scores[0]):
        if idx < len(metadata):
            results.append({
                "match_score": float(score),
                "title": metadata[idx]["Job Title"],
                "company": metadata[idx]["Company"],
                "location": metadata[idx]["location"]
            })
    return results
