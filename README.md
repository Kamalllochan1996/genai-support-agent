# GenAI Support Agent

A production-oriented GenAI Support Agent API built with FastAPI, RAG, ChromaDB, LLM integration, conversation memory, evaluation, Docker, and automated CI.

## Features

- FastAPI REST API
- Retrieval-Augmented Generation (RAG)
- ChromaDB vector store
- Document ingestion and chunking
- Embeddings and semantic retrieval
- LLM integration
- Conversation memory
- SQLite database persistence
- Background job support
- Request logging
- Prometheus metrics
- Health check endpoint
- Automated pytest test suite
- Docker support
- Docker Compose support
- GitHub Actions CI

## Project Structure

```text
genai-support-agent/
│
├── app/
│   ├── agents/
│   ├── api/
│   │   ├── routes/
│   │   └── services/
│   ├── config/
│   ├── core/
│   ├── db/
│   │   ├── repositories/
│   │   └── services/
│   ├── embedding/
│   ├── evaluation/
│   ├── ingestion/
│   │   └── loaders/
│   ├── langchain/
│   ├── llm/
│   ├── memory/
│   ├── rag/
│   ├── retrieval/
│   ├── schemas/
│   ├── tools/
│   └── vectorstore/
│
├── data/
│   └── documents/
│
├── tests/
│   ├── integration/
│   └── unit/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── pytest.ini
├── .dockerignore
├── .gitignore
└── README.md