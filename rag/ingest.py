from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

def ingest_websites():
    with open("rag/websites.txt", "r") as f:
        urls = [line.strip() for line in f.readlines() if line.strip()]

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/114.0.0.0 Safari/537.36"
        )
    }

    all_docs = []

    for url in urls:
        try:
            loader = WebBaseLoader(url, header_template=headers)
            docs = loader.load()
            all_docs.extend(docs)
        except Exception as e:
            print(f"Erro ao carregar {url}: {e}")

    splitter = RecursiveCharacterTextSplitter.from_language(
        language="html", chunk_size=600, chunk_overlap=50
    )
    chunks = splitter.split_documents(all_docs)

    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local("rag/faiss_index")

if __name__ == "__main__":
    load_dotenv()
    ingest_websites()

