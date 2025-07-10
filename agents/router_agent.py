from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from config import model

class RouterAgent:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(model=model, temperature=0)
        self.prompt = PromptTemplate(
            input_variables=["message"],
            template=(
            "You are a routing agent responsible for deciding which type of agent should respond to a question.\n"
            "Your task is to read the user's message and reply with only one of the following agent names:\n"
            "- knowledge → questions about InfinitePay's products, services, or website information.\n"
            "- support → questions or requests regarding the user's account, account creation, balance and transaction history.\n"
            "- slack → if the user wants to talk to a human, is dissatisfied with the service, or if the issue cannot be resolved automatically.\n"
            "- fallback → when it is not possible to decide based on the information or the message is outside the scope of the application.\n\n"
            "User message: {message}\n"
            "Response (only the agent name):\n"
            )
        )

    def route(self, message: str) -> str:
        full_prompt = self.prompt.format(message=message)
        response = self.llm.invoke(full_prompt)

        answer = response.content.strip().lower()

        if "knowledge" in answer:
            return "knowledge"
        elif "support" in answer:
            return "support"
        elif "slack" in answer:
            return "slack"
        else:
            return "fallback"

