# LLM-Based PDF Summarizer

<<<<<<< HEAD
A Streamlit app that summarizes one or more PDF files with Groq LLaMA 3 and lets you ask questions across the uploaded documents.

## Features
- Upload and summarize multiple PDF files in a single run.
- Generate one combined summary from all successfully processed PDFs.
- Ask questions against the uploaded document set with semantic retrieval.
- Skip invalid or unreadable PDFs gracefully and continue with the rest.
- Download the generated summary as a `.txt` file.

## Tech Stack
- Python
- Streamlit
- Groq API
- FAISS
- Sentence Transformers
- PyPDF2 and pdfplumber

## Setup
1. Clone the repository.
2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
3. Activate the environment.
   On Windows PowerShell:
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Create a `.env` file in the project root and add:
   ```env
   GROQ_API_KEY=your_key_here
   ```

## Run The App
```bash
streamlit run app.py
```

## How To Use
1. Upload one or more PDF files.
2. Click `Generate Summary`.
3. Review the combined summary.
4. Ask questions about the uploaded documents.
5. Download the summary if needed.

## Notes
- Text-based PDFs work best. Scanned or image-only PDFs may not extract enough text.
- Very large batches may take longer because each chunk is summarized before the final combined summary is generated.
- If some files fail validation or text extraction, the app will warn you and continue processing the remaining files.
=======
Summarizes PDF documents and answers questions using Groq LLaMA 3.

## Setup
1. Clone the repo
2. Create virtual environment: `python -m venv venv`
3. Install dependencies: `pip install -r requirements.txt`
4. Create `.env` file and add: `GROQ_API_KEY=your_key_here`
5. Run: `streamlit run app.py`
>>>>>>> 0bdfe259bdf50ea9a36e6e46da157dcae7fef47f
