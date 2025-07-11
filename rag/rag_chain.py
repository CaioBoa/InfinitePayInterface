from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from config import model

def load_qa_chain():
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    db = FAISS.load_local("rag/faiss_index", embeddings, allow_dangerous_deserialization=True)
    retriever = db.as_retriever()
    llm = ChatGoogleGenerativeAI(model=model, temperature=0)

    prompt_template = PromptTemplate.from_template(
        """You are an expert assistant for InfinitePay.
            Your job is to help users by answering questions about InfinitePay's services, fees, devices, and support.
            Always respond in fluent and professional English, regardless of the user's language.
            Context:
            {context}
            Question:
            {question}

        Answer:"""
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={"prompt": prompt_template},
        return_source_documents=False,
    )

    return qa_chain

