from io import BytesIO
from pypdf import PdfReader

def extract_text_from_pdf_bytes(pdf_bytes: bytes) -> str:
    reader = PdfReader(BytesIO(pdf_bytes))
    pages = []
    for p in reader.pages:
        text = p.extract_text() or ""
        pages.append(text)
    return "\n\n".join(pages).strip()
