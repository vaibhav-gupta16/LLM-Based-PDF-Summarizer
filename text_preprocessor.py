import re
 
CHUNK_SIZE = 1500  # characters per chunk
OVERLAP    = 150   # overlap between consecutive chunks
 
def clean_text(text: str) -> str:
    """Removes noise from extracted PDF text."""
    text = re.sub(r'\n+', ' ', text)          # collapse newlines
    text = re.sub(r'\s+', ' ', text)           # collapse whitespace
    text = re.sub(r'[^\x00-\x7F]+', ' ', text) # strip non-ASCII
    text = re.sub(r'\s+', ' ', text)
    return text.strip()
 
def normalize_text(text: str) -> str:
    """Basic normalization — lowercase."""
    return text.lower()
 
def chunk_text(text: str,
               chunk_size: int = CHUNK_SIZE,
               overlap: int = OVERLAP) -> list:
    """Splits text into overlapping chunks to handle LLM context limits."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        if chunk.strip():
            chunks.append(chunk.strip())
        start += chunk_size - overlap
    return chunks
 
def preprocess(raw_text: str) -> list:
    """Full pipeline: clean -> chunk."""
    cleaned = clean_text(raw_text)
    return chunk_text(cleaned)
