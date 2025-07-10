import pytest
from fastapi.testclient import TestClient
from main import app
from agents.knowledge_agent import KnowledgeAgent
from agents.support_agent import CustomerSupportAgent
from agents.router_agent import RouterAgent

client = TestClient(app)

def test_knowledge_agent_response():
    agent = KnowledgeAgent()
    response = agent.answer("What are the fees of the Maquininha Smart?")
    assert isinstance(response, str)
    assert any(term in response.lower() for term in ["0.35%", "0,35%"])

def test_customer_support_agent_response():
    agent = CustomerSupportAgent()
    response = agent.handle("I want to know my current balance.","user_1")
    assert isinstance(response, str)
    assert "77" in response

def test_orchestrator_routing_knowledge():
    orchestrator = RouterAgent()
    destination = orchestrator.route("What are the rates for credit card?")
    assert destination == "knowledge"

def test_orchestrator_routing_support():
    orchestrator = RouterAgent()
    destination = orchestrator.route("I want to create a new account.")
    assert destination == "support"

def test_orchestrator_routing_fallback():
    orchestrator = RouterAgent()
    destination = orchestrator.route("Quando foi o último jogo do Palmeiras?")
    assert destination == "fallback"

@pytest.mark.parametrize("payload", [
    {"message": "What are the fees of the Maquininha Smart", "user_id": "client789"},
    {"message": "Do I have an account?", "user_id": "client789"},
    {"message": "Add 37 dollars to my account", "user_id": "client789"},
])

def test_api_chat_endpoint(payload):
    response = client.post("/ask", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert isinstance(data["response"], str)
    assert len(data["response"]) > 5






