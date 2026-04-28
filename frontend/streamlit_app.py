import streamlit as st
import requests

BACKEND_URL = "http://localhost:8000"

st.title("PDF RAG Chatbot")

uploaded_file = st.file_uploader(
    "Upload PDF",
    type=["pdf"]
)

if uploaded_file:
    files = {
        "file": (
            uploaded_file.name,
            uploaded_file,
            "application/pdf"
        )
    }

    response = requests.post(
        f"{BACKEND_URL}/upload",
        files=files
    )

    st.success(
        response.json()["message"]
    )

query = st.text_input(
    "Ask a question from PDF"
)

if st.button("Ask"):
    response = requests.post(
        f"{BACKEND_URL}/ask",
        params={"query": query}
    )

    result = response.json()

    st.write("### Answer")
    st.write(result["answer"])

    st.write("### Citations")
    st.write(result["citations"])
