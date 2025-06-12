import pandas as pd
import numpy as np
import faiss
import pickle
from numpy.typing import NDArray

from ..app.embeddings import embed_text


# Load dataset
df = pd.read_csv("backend/data/jobs.csv")
df = df.fillna("")

# Combine relevant fields
def combine_fields(row):
    return (
        f"{row['Job Title']}. "
        f"{row['Job Description']} "
        f"{row['skills']} "
        f"{row['Responsibilities']} "
        f"{row['Qualifications']}"
    )

df["combined_text"] = df.apply(combine_fields, axis=1)
texts = df["combined_text"].tolist()

# Create embeddings
embeddings = [embed_text(t) for t in texts]

# Convert to NumPy array with correct dtype and shape
embedding_matrix: NDArray[np.float32] = np.array(embeddings, dtype="float32")

# Check shape
print("Embedding matrix shape:", embedding_matrix.shape)

# Create FAISS index
embedding_dim = embedding_matrix.shape[1]
index = faiss.IndexFlatL2(embedding_dim)

# Add embeddings
index.add(embedding_matrix) # type: ignore

# Save index
faiss.write_index(index, "backend/data/faiss_jobs.index")

# Save job metadata
metadata = df[[
    "Job Id", "Job Title", "Company", "location", "Work Type", "Salary Range", "Job Posting Date"
]].to_dict(orient="records")

with open("backend/data/job_metadata.pkl", "wb") as f:
    pickle.dump(metadata, f)

print("FAISS index and metadata saved.")
