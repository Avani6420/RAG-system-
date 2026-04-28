import os
import fitz
import faiss
import pickle
import numpy as np

from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter
from groq import Groq

from config import GROQ_API_KEY, VECTOR_DIR

# Load embedding model
embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Groq client
client = Groq(api_key=GROQ_API_KEY)

# Extract text + metadata
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    full_docs = []
    for page_num, page in enumerate(doc):
        text = page.get_text()
        full_docs.append({
            "text": text,
            "page": page_num + 1
        })
    return full_docs

# Chunking
def chunk_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = []
    for doc in documents:
        split_texts = splitter.split_text(doc["text"])

        for chunk in split_texts:
            chunks.append({
                "text": chunk,
                "page": doc["page"]
            })

    return chunks

# Create FAISS Index
def create_vector_store(chunks):
    texts = [chunk["text"] for chunk in chunks]

    embeddings = embedding_model.encode(texts)

    dimension = embeddings.shape[1]
    print(dimension, "size of embedding")
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings))

    faiss.write_index(
        index,
        f"{VECTOR_DIR}/index.faiss"
    )

    with open(f"{VECTOR_DIR}/metadata.pkl", "wb") as f:
        pickle.dump(chunks, f)

# Retrieve relevant chunks
def retrieve_chunks(query, top_k=3):
    query_embedding = embedding_model.encode([query])

    index = faiss.read_index(
        f"{VECTOR_DIR}/index.faiss"
    )

    with open(f"{VECTOR_DIR}/metadata.pkl", "rb") as f:
        metadata = pickle.load(f)

    distances, indices = index.search(
        np.array(query_embedding),
        top_k
    )
    retrieved_docs = []

    for idx in indices[0]:
        retrieved_docs.append(metadata[idx])

    return retrieved_docs

# Generate answer
def generate_answer(query):
    docs = retrieve_chunks(query)

    context = "\n\n".join(
        [doc["text"] for doc in docs]
    )

    pages = list(set(
        [doc["page"] for doc in docs]
    ))

    prompt = f"""
        Answer ONLY from the provided context.
        Context:
        {context}

        Question:
        {query}
        Also provide concise answer.
        """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    answer = response.choices[0].message.content
    return {
        "answer": answer,
        "citations": pages
    }