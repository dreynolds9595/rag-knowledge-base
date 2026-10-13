import os

# Load API key from Streamlit secrets (cloud) or .env (local)
try:
    import streamlit as st
    if "GROQ_API_KEY" in st.secrets:
        os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
except Exception:
    pass

from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from app.ingest import ingest, collection
from app.pipeline import ask

st.set_page_config(page_title="RAG Knowledge Base", page_icon="📚", layout="wide")
st.title("📚 RAG Knowledge Base")
st.caption("Upload documents, ask questions, get cited answers grounded in your sources.")

with st.sidebar:
    st.header("📄 Documents")
    uploaded = st.file_uploader(
        "Upload PDF, TXT, or MD",
        type=["pdf", "txt", "md"],
        accept_multiple_files=True,
    )
    if uploaded and st.button("Ingest uploads"):
        os.makedirs("data/uploaded", exist_ok=True)
        for f in uploaded:
            with open(f"data/uploaded/{f.name}", "wb") as out:
                out.write(f.getbuffer())
        with st.spinner("Ingesting..."):
            ingest("data/uploaded")
        st.success(f"Ingested {len(uploaded)} file(s).")

    st.divider()
    if st.button("Load sample data"):
        with st.spinner("Loading samples..."):
            ingest("data/sample_docs")
        st.success("Sample data loaded.")

    st.divider()
    st.metric("Chunks in DB", collection.count())

st.header("❓ Ask a Question")
query = st.text_input("Your question:", placeholder="What is retrieval augmented generation?")

if query:
    with st.spinner("Thinking..."):
        result = ask(query)

    st.markdown("### Answer")
    st.markdown(result["answer"])

    if result["sources"]:
        with st.expander("📎 Sources", expanded=False):
            for s in result["sources"]:
                st.markdown(f"**[{s['id']}]** `{s['source']}`")
                st.caption(s["text"] + "...")