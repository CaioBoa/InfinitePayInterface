from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from config import model

def load_qa_chain():
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    db = FAISS.load_local("rag/faiss_index", embeddings, allow_dangerous_deserialization=True)

    retriever = db.as_retriever()

    llm = ChatGoogleGenerativeAI(model=model, temperature=0.2)
    qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
    return qa
