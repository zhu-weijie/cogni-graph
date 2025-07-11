# CogniGraph: A Multi-Tenant AI-Powered Knowledge Assistant

CogniGraph is a scalable, multi-tenant AI platform designed for enterprise clients to securely upload their private documents (PDFs) and query them using natural language. The system leverages a powerful combination of Retrieval-Augmented Generation (RAG) and a Knowledge Graph (KG) to provide accurate, cited, and context-aware answers through an intelligent AI agent.

This project is built using modern, production-grade technologies with a focus on clean architecture, scalability, and robust testing.

## Key Features

- **Multi-Tenant by Design:** Strict data isolation between tenants at the database and API level.
- **Hybrid Search:** Combines semantic vector search (RAG) for broad questions and structured graph search (KG) for specific, factual queries.
- **Intelligent AI Agent:** An LLM-powered agent that analyzes user questions and dynamically chooses the best tool (RAG or KG) to find the answer.
- **Asynchronous Processing:** Document uploads trigger a background Celery task for ingestion, ensuring the API remains responsive.
- **Streaming Responses:** The agent streams answers token-by-token for an interactive user experience.
- **Containerized & Scalable:** Fully containerized with Docker and ready for deployment on Kubernetes.

## Architecture

The application is designed with clean, decoupled architectural layers to ensure maintainability and separation of concerns.

**High-Level System Design:**
![System Architecture Diagram](design/class_diagram.md)

**AI Agent Query Flow:**
This diagram shows how a query is processed by the AI agent, which selects the appropriate tool to generate an answer.
![Agent Sequence Diagram](design/sequence_diagram.md)

## Tech Stack

| Component            | Technology                                | Purpose                                        |
| -------------------- | ----------------------------------------- | ---------------------------------------------- |
| **Backend Framework**| FastAPI                                   | High-performance, asynchronous API             |
| **AI Orchestration** | LangChain                                 | Building agent, tools, and QA chains           |
| **LLM Provider**     | OpenAI (gpt-4o)                           | AI reasoning, generation, and graph extraction |
| **Relational DB**    | PostgreSQL                                | Tenant metadata management                     |
| **Vector Store**     | PGVector                                  | Storing and searching document embeddings (RAG)|
| **Graph DB**         | Neo4j (with APOC plugin)                  | Storing and querying the Knowledge Graph (KG)  |
| **Async Tasks**      | Celery & Redis                            | Background processing for document ingestion   |
| **Containerization** | Docker & Docker Compose                   | Local development and production builds        |
| **Testing**          | Pytest, Pytest-Mock                       | Unit and integration testing                   |
| **Dependency Mgmt**  | pip-tools                                 | Reproducible, locked dependencies              |

## Local Setup & Usage

### Prerequisites
- Docker and Docker Compose
- Python 3.12
- An OpenAI API key

### Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd cogni-graph
    ```

2.  **Create the environment file:**
    Create a `.env` file in the project root and add your OpenAI API key:
    ```
    OPENAI_API_KEY="sk-..."
    ```

3.  **Build and start the services:**
    This command will build the Docker images and start all services (API, worker, Postgres, Neo4j, Redis).
    ```bash
    docker compose up -d --build
    ```

4.  **Access the services:**
    - **API Docs:** `http://localhost:8000/docs`
    - **Neo4j Browser:** `http://localhost:7474` (Connect to `neo4j://localhost:7687` with user `neo4j` and password `password`)

### API Endpoints Walkthrough

First, get a `TENANT_ID` to use in the following commands:
```bash
TENANT_ID=$(curl -s -X POST "http://127.0.0.1:8000/tenants/" -H "Content-Type: application/json" -d '{"name": "My Test Tenant"}' | grep -o '"id":"[^"]*' | cut -d'"' -f4)
echo "Using TENANT_ID: $TENANT_ID"
```

**1. Upload a Document (Async)**
This will upload the `bitcoin.pdf` and start background processing.
```bash
TASK_ID=$(curl -s -X POST "http://127.0.0.1:8000/tenants/$TENANT_ID/upload" -F "file=@bitcoin.pdf" | grep -o '"task_id":"[^"]*' | cut -d'"' -f4)
echo "Started processing with Task ID: $TASK_ID"
```

**2. Check Processing Status**
Wait a few moments and check the status of the task.
```bash
curl "http://127.0.0.1:8000/tenants/$TENANT_ID/status/$TASK_ID"
```

**3. Query the Agent (Streaming)**
Once processing is complete, ask the agent a question.
```bash
# General question (uses RAG)
curl -N -X POST "http://127.0.0.1:8000/tenants/$TENANT_ID/query/" \
-H "Content-Type: application/json" \
-d '{"query": "What is a blockchain?"}'

# Specific question (uses Knowledge Graph)
curl -N -X POST "http://127.0.0.1:8000/tenants/$TENANT_ID/query/" \
-H "Content-Type: application/json" \
-d '{"query": "Who is the author of the bitcoin paper?"}'
```

## Testing

This project uses `pytest` for both unit and integration tests.

To run the full test suite in an isolated environment:
```bash
docker compose -f docker-compose.testing.yml run --rm tester
```
