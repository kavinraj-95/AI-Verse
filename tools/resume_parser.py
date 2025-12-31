import pypdf
from typing import IO

def resume_parser(file: IO[bytes]) -> str:
    """
    Parses a PDF resume file and returns the text content.
    """
    try:
        pdf_reader = pypdf.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        return f"Error parsing PDF: {e}"

