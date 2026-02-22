import os
 
MAX_SIZE_MB = 10
 
def validate_pdf(file_path: str) -> dict:
    """Validates that the uploaded file is a valid PDF within size limits."""
    result = {"valid": False, "message": ""}
 
    if not os.path.exists(file_path):
        result["message"] = "File not found."
        return result
 
    # Check file extension
    if not file_path.lower().endswith('.pdf'):
        result["message"] = "File must have a .pdf extension."
        return result
 
    # Check magic bytes (PDF starts with %PDF)
    with open(file_path, "rb") as f:
        header = f.read(4)
    if header != b'%PDF':
        result["message"] = "File is not a valid PDF (invalid header)."
        return result
 
    # Check file size
    size_mb = os.path.getsize(file_path) / (1024 * 1024)
    if size_mb > MAX_SIZE_MB:
        result["message"] = f"File size ({size_mb:.1f}MB) exceeds {MAX_SIZE_MB}MB limit."
        return result
 
    result['valid'] = True
    result["message"] = f"Valid PDF ({size_mb:.2f} MB)"
    return result
