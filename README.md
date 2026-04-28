📄 PDF RAG Chatbot (End-to-End Retrieval Augmented Generation System)
An end-to-end **Document Question Answering System** built using **FastAPI, FAISS, HuggingFace Embeddings, Groq LLM, and Streamlit**.
This project allows users to upload PDF documents and ask questions based on document content using Retrieval-Augmented Generation (RAG).

🚀 Features
- Upload PDF documents
- Extract text from PDFs
- Smart text chunking
- Generate embeddings using HuggingFace models
- Store embeddings in FAISS vector database
- Retrieve relevant chunks
- Generate answers using LLM
- Citation support (page numbers)
- Streamlit chat UI
- FastAPI backend
- Free API integration (Groq)

🏗️ Architecture
User Upload PDF
      ↓
Text Extraction
      ↓
Text Chunking
      ↓
Embedding Generation
      ↓
FAISS Vector Storage
      ↓
Question Query
      ↓
Similarity Search
      ↓
LLM Response Generation
      ↓
Answer + Citations

🛠 Tech Stack
Backend:
  FastAPI
  Python
LLM Framework:
  LangChain
Embeddings:
  HuggingFace Sentence Transformers
Vector Database:
  FAISS
LLM:
  Groq API (Free Tier)
Frontend:
  Streamlit
PDF Processing:
  PyMuPDF

Project structure:
rag_pdf_chatbot/
│
├── backend/
│   ├── app.py
│   ├── rag_pipeline.py
│   ├── config.py
│   ├── requirements.txt
│
├── frontend/
│   ├── streamlit_app.py
│
├── uploaded_docs/
├── vector_store/
├── .env
└── README.md

Installation
1. Clone Repository:
   git clone https://github.com/yourusername/rag_pdf_chatbot.git
   cd rag_pdf_chatbot
2. Create Virtual Environment: python -m venv venv
3. Install Dependencies: pip install -r backend/requirements.txt
4. Setup Environment Variables:
      Create .env file inside project root:
       GROQ_API_KEY=your_groq_api_key_here
5. Run Application:
   Start FastAPI Backend:
       cd backend
       uvicorn app:app --reload
6. Start Streamlit Frontend:
    cd frontend
    streamlit run streamlit_app.py
