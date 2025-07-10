from rag.rag_chain import load_qa_chain

class KnowledgeAgent:
    def __init__(self):
        self.qa = load_qa_chain()

    def answer(self, message: str) -> str:
        result = self.qa.invoke(message)
        return result["result"]
