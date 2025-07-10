# InfinitePay Agent Swarm

A multi-agent chatbot system designed to answer questions about InfinitePay’s products and services and to allow users to check, update, or create their account data. Built with modular agents and powered by LLMs, the system features intelligent routing, RAG-based knowledge responses, support action emulation, tone customization, and toxicity filtering.

---

## Main Tools

* **LangChain**: for prompt chaining, agent orchestration, and RAG construction
* **GeminiAI (Google Generative AI)**: as the core LLM for reasoning and generation
* **FastAPI**: backend HTTP API service to handle message routing and processing
* **Docker & Docker Compose**: to containerize the application for scalable deployment
* **Streamlit**: frontend interface for user interaction with the agent system

---

## Agent Roles

* **RouterAgent**: Entry point that classifies the incoming message via LLM and determines the processing agent.

* **KnowledgeAgent**: Responds to questions regarding InfinitePay’s services and products using a RAG chain grounded in scraped website content.

* **CustomerSupportAgent**: Handles support requests and manipulates mock user data using structured outputs.

  This agent operates over a `.json` file (`mock_users.json`) to emulate a simple database structure. Each user is identified by a `user_id`, which stores their current balance and transaction history.

  It uses three tools internally:

  * `create_new_user`: Initializes a new user with default balance and empty transactions.
  * `add_balance`: Applies deposits to the user balance and adds a transactions to its transaction history.
  * `debit_balance`: Applies debits to the user balance and adds a transactions to its transaction history.

  The agent uses a `Pydantic` model (`SupportAction`) to define and parse the expected response structure. This model includes flags for supported actions (e.g., `create_user`, `add_balance`, `debit_balance`), a numeric `amount`, and a natural language `final_response`. This structured design consolidates multiple potential operations into a single agent without requiring a chain of multiple LLM calls, thus improving latency and simplifying the architecture.

* **SlackAgent**: Simulates escalation to human support using webhook or terminal log.

* **PersonalityAgent**: Stylizes the final response using LLM prompt injection to reflect the user’s tone.

* **ToxicityDetector**: Filters inappropriate inputs using `unitary/toxic-bert`.

### Message Flow

1. User submits a query via the Streamlit interface.
2. Request reaches the FastAPI `/ask` endpoint.
3. Guardrails module detects toxicity (blocked if malicious).
4. RouterAgent chooses the right agent (knowledge, support, slack, or fallback).
5. Specialized agent processes the input and returns a response.
6. PersonalityAgent rephrases the response in the desired tone.
7. Final response, original response, and workflow trace are returned in a JSON.

**Example Response:**

```json
{
  "response": "The personality-infused reply or final output",
  "source_agent_response": "The original response from RAG Agent before personality was applied.",
  "agent_workflow": [
    {"agent_name": "support", "tool_calls": {"create_user": true}}
  ]
}
```

---

## Retrieval-Augmented Generation (RAG) Pipeline

### Data Ingestion

The `ingest.py` script performs the following steps:

1. Load URLs from `rag/websites.txt`.
2. Scrape pages using `WebBaseLoader` with a custom user-agent.
3. Split HTML content using `RecursiveCharacterTextSplitter`.
4. Embed text chunks using `GoogleGenerativeAIEmbeddings`.
5. Store the resulting vectors in a FAISS local index (`rag/faiss_index`).

### Query Processing

The `KnowledgeAgent` loads the FAISS index and creates a `RetrievalQA` chain:

* Uses top-k retrieved documents as context
* Uses LLM to synthesize a grounded answer
* Returns the base response for further personality transformation

---

## 🔧 Testing Strategy

### How to Run

```bash
pytest test_app.py
```

### Unit Tests

* `KnowledgeAgent`: validates output contains key factual elements (e.g., fees)
* `CustomerSupportAgent`: checks account creation, balance updates, debits
* `RouterAgent`: validates intent routing logic based on LLM prompt output

### End-to-End Tests

* JSON POST tests on `/ask` endpoint
* Multiple user scenarios covering all three main agents

### Future Integration Tests

* SlackAgent webhook validation
* Guardrail trigger verification
* SupportAgent data integrity checks using mock JSON database

---
