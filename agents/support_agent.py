import json
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from typing import Optional
from config import model

class SupportAction(BaseModel):
    create_user: bool = False
    add_balance: bool = False
    debit_balance: bool = False
    amount: Optional[float] = 0.0
    final_response: str

class CustomerSupportAgent:
    def __init__(self, user_data_path="data/mock_users.json"):
        with open(user_data_path, "r", encoding="utf-8") as f:
            self.users = json.load(f)

        self.llm = ChatGoogleGenerativeAI(model=model, temperature=0)
        self.parser = PydanticOutputParser(pydantic_object=SupportAction)   

        self.prompt = ChatPromptTemplate.from_template(
            template=(
                "You are a support agent for InfinitePay.\n"
                "Based on the data below and the user's message, identify the intended actions and provide a personalized response.\n\n"
                "USER DATA (or 'N/A' if not available):\n{user_data}\n\n"
                "USER MESSAGE:\n{message}\n\n"
                "If the user wants to create an account, set create_user to true\n"
                "If the user wants to add balance, set add_balance to true and amount to the value to be added\n"
                "If the user wants to debit balance, set debit_balance to true and amount to the value to be debited\n\n"
                "Respond ONLY with a valid JSON in the following format:\n"
                "{{\n"
                "  \"create_user\": true/false,\n"
                "  \"add_balance\": true/false,\n"
                "  \"debit_balance\": true/false,\n"
                "  \"amount\": number (estimated value),\n"
                "  \"final_response\": \"personalized response to the user\"\n"
                "}}\n"
                "Respond in the same language as the message received."
            )
        )
        self.chain = self.prompt | self.llm | self.parser

    def handle(self, message: str, user_id: str) -> str:
        user = self.users.get(user_id)
        user_data_str = self.format_user_data(user) if user else "N/A"

        try:
            parsed = self.chain.invoke({"user_data": user_data_str, "message": message})
        except Exception as e:
            print("Parsing Error:", e)
            return "There was an error interpreting the agent's response."
        print("Parsed response:", parsed)

        if parsed.create_user and user_id not in self.users:
            return self.create_new_user(user_id)

        if parsed.add_balance and user_id in self.users:
            return self.add_balance(user_id, parsed.amount)

        if parsed.debit_balance and user_id in self.users:
            return self.debit_balance(user_id, parsed.amount)

        return parsed.final_response if user else "User not Found."

    def create_new_user(self, user_id: str) -> str:
        default_user_data = {
            "balance": 0.0,
            "transactions": []
        }
        self.users[user_id] = default_user_data
        self.save_users()
        return "Account successfully created!"

    def add_balance(self, user_id: str, amount: float) -> str:
        self.users[user_id]["balance"] += amount
        self.users[user_id]["transactions"].insert(0, {
            "type": "deposit",
            "value": amount
        })
        self.save_users()
        return f"Balance updated! Your new balance is R$ {self.users[user_id]['balance']:.2f}."

    def debit_balance(self, user_id: str, amount: float) -> str:
        user = self.users[user_id]
        if user["balance"] < amount:
            return f"Insufficient balance! Your current balance is R$ {user['balance']:.2f}."
        user["balance"] -= amount
        user["transactions"].insert(0, {
            "type": "debit",
            "value": -amount
        })
        self.save_users()
        return f"Debit completed! Your new balance is R$ {user['balance']:.2f}."

    def format_user_data(self, user: dict) -> str:
        if not user:
            return "N/A"
        balance = f"Balance: R$ {user['balance']:.2f}"
        txs = "\n".join([
            f"- R$ {t['value']:.2f} via {t['type']}" for t in user.get("transactions", [])
        ])
        return f"{balance}\nTransactions:\n{txs}"

    def save_users(self):
        with open("data/mock_users.json", "w", encoding="utf-8") as f:
            json.dump(self.users, f, indent=2, ensure_ascii=False)




