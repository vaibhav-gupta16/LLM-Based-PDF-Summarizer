import PyPDF2
import pdfplumber
 
def extract_text(file_path: str) -> str:
    """Extracts raw text from a PDF using PyPDF2 with pdfplumber fallback."""
    text = ""
    try:
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception:
        pass
 
    # Fallback to pdfplumber if PyPDF2 yields little text
    if len(text.strip()) < 100:
        text = ""
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            return f"Error extracting text: {str(e)}"
 
    return text.strip()
