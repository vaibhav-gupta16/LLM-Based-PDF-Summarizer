import streamlit as st
st.set_page_config(page_title="LLM PDF Summarizer", page_icon="📄", layout="wide")
import tempfile
import os
from pdf_validator     import validate_pdf
from text_extractor    import extract_text
from text_preprocessor import preprocess
from summarizer        import generate_summary
from qa_engine         import QAEngine
 
# ── Custom CSS ────────────────────────────────────────────────────
st.markdown('''
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
</style>''', unsafe_allow_html=True)
 
st.title("📄 LLM-Based PDF Summarizer")
st.markdown(
    'Upload a PDF document to get an **AI-generated summary** '
    'and **ask questions** about its content.'
)
 
# ── Session state ─────────────────────────────────────────────────
if "summary"   not in st.session_state: st.session_state.summary   = None
if "qa_engine" not in st.session_state: st.session_state.qa_engine = None
if "chunks"    not in st.session_state: st.session_state.chunks    = None
 
# ── File upload ───────────────────────────────────────────────────
uploaded_file = st.file_uploader(
    "Upload PDF File",
    type=["pdf"],
    help="Max file size: 10 MB"
)
 
if uploaded_file is not None:
    # Save to a temp file so our modules can read it from disk
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name
 
    # ── Step 1: Validate ──────────────────────────────────────────
    with st.spinner('Validating PDF...'):
        validation = validate_pdf(tmp_path)
 
    if not validation['valid']:
        st.error(f"❌ Invalid PDF: {validation['message']}")
        os.unlink(tmp_path)
    else:
        st.success(f"✅ {validation['message']}")
        col1, col2 = st.columns([1, 1])
 
        with col1:
            generate_btn = st.button(
                "🔍 Generate Summary",
                type="primary",
                use_container_width=True
            )
 
        if generate_btn:
            # ── Step 2: Extract ───────────────────────────────────
            with st.spinner('Extracting text from PDF...'):
                raw_text = extract_text(tmp_path)
 
            if not raw_text or len(raw_text) < 50:
                st.error('Could not extract text. '
                         "The PDF may be scanned/image-based.")
            else:
                # ── Step 3: Preprocess ────────────────────────────
                with st.spinner('Preprocessing text...'):
                    chunks = preprocess(raw_text)
                    st.session_state.chunks = chunks
                st.info(f'Processing {len(chunks)} text chunk(s)...')
 
                # ── Step 4: Summarise ─────────────────────────────
                with st.spinner(
                    'Generating summary'
                    '(may take 30–60 s on first run)...'
                ):
                    summary = generate_summary(chunks)
                    st.session_state.summary = summary
 
                # ── Step 5: Build Q&A index ───────────────────────
                with st.spinner('Building Q&A vector index...'):
                    st.session_state.qa_engine = QAEngine(chunks)
 
                st.success('✅ Summary generated!')
 
        # ── Download button ───────────────────────────────────────
        with col2:
            if st.session_state.summary:
                st.download_button(
                    "⬇️ Download Summary (.txt)",
                    data=st.session_state.summary,
                    file_name="summary.txt",
                    mime="text/plain",
                    use_container_width=True
                )
 
        # ── Display summary ───────────────────────────────────────
        if st.session_state.summary:
            st.subheader("📋 Generated Summary")
            st.markdown(
                f'<div class="summary-box">{st.session_state.summary}</div>',
                unsafe_allow_html=True
            )
            st.markdown('---')
 
            # ── Q&A section ───────────────────────────────────────
            st.subheader("💬 Ask a Question About the Document")
            question = st.text_input(
                "Your question:",
                placeholder="What is the main topic of this document?"
            )
            if st.button('Get Answer') and question:
                with st.spinner('Finding answer...'):
                    answer = st.session_state.qa_engine.answer(question)
                st.markdown(
                    f'<div class="answer-box"><b>Answer:</b> {answer}</div>',
                    unsafe_allow_html=True
                )
 
        # Cleanup temp file
        try:
            os.unlink(tmp_path)
        except Exception:
            pass
 
st.markdown('---')