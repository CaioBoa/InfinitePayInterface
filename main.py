from fastapi import FastAPI, Request
from pydantic import BaseModel
from agents.router_agent import RouterAgent
from agents.knowledge_agent import KnowledgeAgent
from agents.support_agent import CustomerSupportAgent
from agents.personality_layer import PersonalityAgent
from agents.slack_agent import SlackAgent
from dotenv import load_dotenv
from guardrails.toxicity_checker import ToxicityDetector
from config import test

if test:
    import os
    os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

app = FastAPI()
load_dotenv()

router = RouterAgent()
knowledge_agent = KnowledgeAgent()
support_agent = CustomerSupportAgent()
slack_agent = SlackAgent()
personality = PersonalityAgent()
tox_checker = ToxicityDetector()

class MessageInput(BaseModel):
    message: str
    user_id: str
    tone: str = "professional"

@app.post("/ask")
async def ask(input: MessageInput):

    if tox_checker.is_malicious(input.message):
        response = "Sorry, your message contains inappropriate content and could not be processed."
        return {
        "response": response,
        "source_agent_response": response,
        "agent_workflow": [
            {"agent_name": "blocked by guardrails"}
        ]
    }
    
    print(f"Received message: {input.message} from user: {input.user_id}")
    route = router.route(input.message)
    print(f"Routed to: {route}")

    tools = []

    if route == "knowledge":
        response = knowledge_agent.answer(input.message)
    elif route == "support":
        raw_response = support_agent.handle(input.message, input.user_id)
        response = raw_response["answer"]
        tools = raw_response["tools"]
    elif route == "slack":
        response = slack_agent.handle(input.message, input.user_id)
    else:
        response = "Sorry, I couldn't understand your question."

    final_response = personality.apply(response, input.tone)

    return {
        "response": final_response,
        "source_agent_response": response,
        "agent_workflow": [
            {"agent_name": route, "tools": tools},
            {"agent_name": "personality", "tools": []}
        ]
    }