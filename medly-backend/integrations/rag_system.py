from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
import os

def setup_rag():
    documents = []
    for filename in os.listdir("research_papers"):
        if filename.endswith(".pdf"):
            loader = PyPDFLoader(f"research_papers/{filename}")
            documents.extend(loader.load())
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(documents)
    embeddings = OpenAIEmbeddings()
    vector_store = FAISS.from_documents(chunks, embeddings)
    return vector_store

vector_store = setup_rag()

def query_rag(query: str) -> str:
    results = vector_store.similarity_search(query, k=3)
    return "\n".join([doc.page_content for doc in results]) 
