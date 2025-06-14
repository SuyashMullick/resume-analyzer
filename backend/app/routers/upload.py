from fastapi import APIRouter, UploadFile, File, HTTPException
from ..resume_parser import extract_text_from_pdf
from ..embeddings import embed_text

router = APIRouter()

@router.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    if not file.filename or not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    contents = await file.read()

    extracted_text = extract_text_from_pdf(contents)

    if not extracted_text:
        raise HTTPException(status_code=500, detail="Failed to extract text from the PDF.")

    embedding = embed_text(extracted_text)

    return {
        "status": "success",
        "filename": file.filename,
        "text_preview": extracted_text[:500] + "...",
        "length": len(extracted_text.split()),
        "embedding_dim": len(embedding)
    }
