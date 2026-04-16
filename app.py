import os
import tempfile
import streamlit as st
from pdf_validator import validate_pdf
from qa_engine import QAEngine
from summarizer import generate_summary
from text_extractor import extract_text
from text_preprocessor import preprocess

st.set_page_config(page_title="LLM PDF Summarizer", page_icon="PDF", layout="wide")

st.markdown(
    """
<style>
  .block-container { padding-top: 2rem; }
  .summary-box {
    background: #1e2a3a;
    color: #e8f0fe;
    padding: 20px;
    border-radius: 8px;
    border-left: 4px solid #4da6ff;
    font-size: 15px;
    line-height: 1.8;
  }
  .answer-box {
    background: #1a2e1a;
    color: #b7f0b7;
    padding: 14px;
    border-radius: 8px;
    border-left: 4px solid #28a745;
    font-size: 15px;
  }
</style>
""",
    unsafe_allow_html=True,
)


def reset_results() -> None:
    st.session_state.summary = None
    st.session_state.qa_engine = None
    st.session_state.chunks = []
    st.session_state.processed_files = []


def process_uploaded_pdfs(uploaded_files):
    all_chunks = []
    processed_files = []
    skipped_files = []
    temp_paths = []

    try:
        for uploaded_file in uploaded_files:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(uploaded_file.getbuffer())
                tmp_path = tmp.name
            temp_paths.append(tmp_path)

            validation = validate_pdf(tmp_path)
            if not validation["valid"]:
                skipped_files.append(f"{uploaded_file.name}: {validation['message']}")
                continue

            raw_text = extract_text(tmp_path)
            if not raw_text or len(raw_text.strip()) < 50:
                skipped_files.append(
                    f"{uploaded_file.name}: Could not extract enough readable text."
                )
                continue

            chunks = preprocess(raw_text)
            if not chunks:
                skipped_files.append(
                    f"{uploaded_file.name}: No usable text chunks were produced."
                )
                continue

            labeled_chunks = [
                f"Document: {uploaded_file.name}\n\n{chunk}" for chunk in chunks
            ]
            all_chunks.extend(labeled_chunks)
            processed_files.append(uploaded_file.name)
    finally:
        for temp_path in temp_paths:
            try:
                os.unlink(temp_path)
            except OSError:
                pass

    return all_chunks, processed_files, skipped_files


if "summary" not in st.session_state:
    reset_results()

st.title("LLM-Based PDF Summarizer")
st.markdown(
    "Upload one or more PDF files to generate a combined **AI summary** and "
    "**ask questions** across all processed documents."
)

uploaded_files = st.file_uploader(
    "Upload PDF file(s)",
    type=["pdf"],
    accept_multiple_files=True,
    help="You can upload and summarize multiple PDF files in one run.",
)

if uploaded_files:
    current_file_names = [file.name for file in uploaded_files]
    if current_file_names != st.session_state.get("processed_files", []):
        reset_results()

    st.caption(f"{len(uploaded_files)} file(s) selected")
    st.write(", ".join(current_file_names))

    col1, col2 = st.columns([1, 1])

    with col1:
        generate_btn = st.button(
            "Generate Summary",
            type="primary",
            use_container_width=True,
        )

    if generate_btn:
        with st.spinner("Validating, extracting, and preprocessing PDFs..."):
            chunks, processed_files, skipped_files = process_uploaded_pdfs(uploaded_files)

        if skipped_files:
            for skipped_file in skipped_files:
                st.warning(skipped_file)

        if not processed_files:
            st.error("No valid PDF files were available to summarize.")
        else:
            st.session_state.chunks = chunks
            st.session_state.processed_files = processed_files
            st.success(f"Ready to summarize {len(processed_files)} PDF file(s).")
            st.info(f"Processing {len(chunks)} text chunk(s) from the uploaded files.")

            with st.spinner("Generating summary (this may take a minute)..."):
                st.session_state.summary = generate_summary(chunks)

            with st.spinner("Building Q&A vector index..."):
                st.session_state.qa_engine = QAEngine(chunks)

            st.success("Summary generated successfully.")

    with col2:
        if st.session_state.summary:
            st.download_button(
                "Download Summary (.txt)",
                data=st.session_state.summary,
                file_name="multi_pdf_summary.txt",
                mime="text/plain",
                use_container_width=True,
            )

    if st.session_state.summary:
        st.subheader("Processed Files")
        st.write(", ".join(st.session_state.processed_files))

        st.subheader("Generated Summary")
        st.markdown(
            f'<div class="summary-box">{st.session_state.summary}</div>',
            unsafe_allow_html=True,
        )
        st.markdown("---")

        st.subheader("Ask a Question About the Documents")
        question = st.text_input(
            "Your question:",
            placeholder="What are the common themes across these files?",
        )
        if st.button("Get Answer") and question:
            with st.spinner("Finding answer..."):
                answer = st.session_state.qa_engine.answer(question)
            st.markdown(
                f'<div class="answer-box"><b>Answer:</b> {answer}</div>',
                unsafe_allow_html=True,
            )

st.markdown("---")
