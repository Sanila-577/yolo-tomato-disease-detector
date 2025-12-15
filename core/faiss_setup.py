import os
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

PDF_FOLDER = "./context"
FAISS_PATH = "./faiss_db"

def build_or_load_faiss():
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    if os.path.exists(FAISS_PATH) and os.listdir(FAISS_PATH):
        print("📂 Loading existing FAISS index...")
        vectorstore = FAISS.load_local(FAISS_PATH, embeddings)
    else:
        print("⚡ Building FAISS index from PDFs...")
        pdf_files = [os.path.join(PDF_FOLDER,f) for f in os.listdir(PDF_FOLDER) if f.endswith(".pdf")]
        docs = []
        for pdf in pdf_files:
            loader = PyPDFLoader(pdf)
            docs.extend(loader.load())

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap = 150)
        splits = text_splitter.split_documents(docs)

        vectorstore = FAISS.from_documents(splits, embedding=embeddings)

        os.makedirs(FAISS_PATH,exist_ok = True)
        vectorstore.save_local(FAISS_PATH)
        print(f"FAISS index saved to {FAISS_PATH}")

    retriever = vectorstore.as_retriever(search_kwargs={"k":5})
    return retriever

