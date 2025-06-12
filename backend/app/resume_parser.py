import pdfplumber
from io import BytesIO

def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    try:
        with pdfplumber.open(BytesIO(pdf_bytes)) as pdf:
            text = ''
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + '\n'
        return text.strip()
    except Exception as e:
        print(f"[ERROR] PDF extraction failed: {e}")
        return ''
