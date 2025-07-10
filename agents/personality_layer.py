from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from config import model

class PersonalityAgent:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(model=model, temperature=0.4)
        self.prompt_template = PromptTemplate(
            input_variables=["tone", "response"],
            template=(
            "You are an assistant that rewrites responses to users, applying different personality styles.\n"
            "Your job is to rewrite the response below according to the indicated tone.\n\n"
            "You must return ONLY ONE response with the described personality.\n"
            "DESIRED TONE: {tone}\n\n"
            "ORIGINAL RESPONSE: {response}\n\n"
            "Always answer in English"
            )
        )

    def apply(self, base_response: str, tone: str) -> str:
        prompt = self.prompt_template.format(tone=tone, response=base_response)
        result = self.llm.invoke(prompt)
        return result.content.strip()