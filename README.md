# LLM-Based PDF Summarizer

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
- pypdf and pdfplumber

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
   ```powershell
   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt
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
- This project now uses Groq for both summarization and question answering. The older Hugging Face, FAISS, and NumPy retrieval stack has been removed.
- This project is set up to work with current Python releases by using modern dependency ranges instead of old strict pins.
- Text-based PDFs work best. Scanned or image-only PDFs may not extract enough text.
- Very large batches may take longer because each chunk is summarized before the final combined summary is generated.
- If some files fail validation or text extraction, the app will warn you and continue processing the remaining files.
