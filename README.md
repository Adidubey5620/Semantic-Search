# Semantic Search API & UI

A complete semantic search application featuring a FastAPI backend and a Streamlit frontend. It utilizes modern transformer-based embeddings and PostgreSQL's `pgvector` extension with HNSW indexing for high-performance vector search.

```
                         ┌─────────────────────┐
                         │   Streamlit (UI)    │
                         └──────────┬──────────┘
                                    │ HTTP
                     POST /documents│ POST /documents/search
                                    ↓
                         ┌─────────────────────┐
                         │      FastAPI        │
                         └──────────┬──────────┘
                                    │
                                    ↓
                         ┌─────────────────────┐
                         │ BGE-small-en-v1.5   │
                         │    384 dimensions   │
                         └──────────┬──────────┘
                                    │
                                    ↓
                         ┌─────────────────────┐
                         │ PostgreSQL (pgvector)│
                         │                     │
                         │ content             │
                         │ embedding vector384 │
                         └──────────┬──────────┘
                                    │
                                    ↓
                                pgvector
                                    │
                                    ↓
                               HNSW index
```

---

## 🚀 Features

- **Interactive UI**: A user-friendly Streamlit frontend to index new documents and perform semantic searches.
- **Text Embeddings**: Automatically generates dense vector representations using `BAAI/bge-small-en-v1.5` (384 dimensions) via `sentence-transformers`.
- **Hybrid Search Capabilities**: Search documents using cosine similarity with additional metadata filters (`category` and `source`).
- **Optimized Vector Search**: Utilizes PostgreSQL `pgvector` with HNSW (Hierarchical Navigable Small World) index for fast, low-latency nearest-neighbor search.
- **Asynchronous Stack**: End-to-end async implementation using `FastAPI`, `SQLAlchemy`, and `asyncpg`.
- **Robust Schema Validation**: Employs Pydantic v2 schemas for strict input validation and responses.

---

## 🛠️ Technology Stack

- **Frontend**: [Streamlit](https://streamlit.io/)
- **Backend Framework**: [FastAPI](https://fastapi.tiangolo.com/) (Async API development)
- **Database**: PostgreSQL with [pgvector](https://github.com/pgvector/pgvector)
- **ORM / Driver**: [SQLAlchemy 2.0](https://www.sqlalchemy.org/) (Async) & [asyncpg](https://github.com/MagicStack/asyncpg)
- **NLP / Embedding Model**: [Sentence-Transformers](https://sbert.net/) (`BAAI/bge-small-en-v1.5`)
- **Settings & Validation**: [Pydantic Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)
- **Package Manager**: [uv](https://github.com/astral-sh/uv)
- **Testing**: [pytest](https://docs.pytest.org/) & [httpx](https://www.python-httpx.org/)

---

## 📁 Directory Structure

```text
├── app/
│   ├── api/
│   │   └── routes/
│   │       ├── documents.py         # Routes for document indexing & search
│   │       └── health.py            # API health check endpoint
│   ├── core/
│   │   ├── config.py                # Environment configuration settings
│   │   ├── exceptions.py            # Domain-specific custom exceptions
│   │   ├── exception_handlers.py    # Custom FastAPI error handlers
│   │   └── logging.py               # Application-wide logger config
│   ├── embeddings/
│   │   └── service.py               # Hugging Face BGE embedding generator
│   ├── services/
│   │   └── document_service.py      # Core database transactions & search queries
│   ├── database.py                  # Async engine and database session setup
│   ├── main.py                      # FastAPI application definition
│   ├── models.py                    # SQLAlchemy Models (pgvector mappings)
│   ├── schemas.py                   # Pydantic validation schemas
│   └── scripts/
│       └── inspect_vector_search.py # Diagnoses explain plans & similarity
├── ui/                              # Streamlit Frontend
│   ├── api.py                       # API client for interacting with FastAPI
│   └── main.py                      # Streamlit application UI
├── tests/                           # Pytest suites
│   ├── conftest.py
│   ├── test_document_service.py
│   ├── test_integration.py
│   └── test_schemas.py
├── pyproject.toml                   # Project metadata and dependencies
└── .env                             # Environment variables configuration
```

---

## ⚙️ Setup & Installation

### 1. Prerequisites
- **Python**: `>= 3.12`
- **PostgreSQL**: `>= 15` with the `pgvector` extension installed.

### 2. Configure Environment Variables
Create a `.env` file in the root directory:

```env
DATABASE_URL=postgresql://<username>:<password>@<host>:<port>/<dbname>
HNSW_EF_SEARCH=40
HF_TOKEN=your_hugging_face_token_if_needed
API_BASE_URL=http://127.0.0.1:8000
```

### 3. Install Dependencies
This project uses `uv` for fast dependency management. If you don't have `uv` installed, get it via pip:
```bash
pip install uv
```

Install workspace dependencies and activate the virtual environment:
```bash
uv venv
# On Windows (PowerShell):
.venv\Scripts\Activate.ps1
# On Linux/macOS:
source .venv/bin/activate

uv sync
```

---

## 🖥️ Running the Application

You need to run both the FastAPI backend and the Streamlit frontend.

### 1. Start the FastAPI Backend

Run the backend server locally using Uvicorn:

```bash
uvicorn app.main:app --reload
```
The API interactive documentation will be available at:
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### 2. Start the Streamlit Frontend

Open a new terminal, activate the virtual environment, and run:

```bash
uv run streamlit run ui/main.py
```
The interactive UI will open in your browser, typically at [http://localhost:8501](http://localhost:8501).

---

## 🔌 API Endpoints

### 1. Index Document
Generates text embedding and stores it in the database.
- **Endpoint**: `POST /documents/`
- **Request Body**:
  ```json
  {
    "content": "FastAPI is a modern, fast (high-performance), web framework for building APIs with Python.",
    "category": "technology",
    "source": "fastapi_docs"
  }
  ```
- **Response**: `201 Created`

### 2. Retrieve All Documents
- **Endpoint**: `GET /documents/`
- **Response**: `200 OK`

### 3. Search Documents
Performs vector similarity search.
- **Endpoint**: `POST /documents/search`
- **Request Body**:
  ```json
  {
    "query": "FastAPI web framework",
    "limit": 5,
    "offset": 0,
    "min_score": 0.5,
    "category": "technology",
    "source": "fastapi_docs"
  }
  ```
- **Response**: `200 OK`
  ```json
  {
    "results": [
      {
        "id": 1,
        "content": "FastAPI is a modern, fast (high-performance), web framework for building APIs with Python.",
        "category": "technology",
        "source": "fastapi_docs",
        "score": 0.8924
      }
    ],
    "count": 1
  }
  ```

---

## 🧪 Testing

Run tests with `pytest`:

```bash
pytest
```

---

## 🔍 Database Diagnostics & Inspect Scripts
To view top semantic results directly via terminal and inspect `EXPLAIN ANALYZE` query plans for index utilization:

```bash
python -m app.scripts.inspect_vector_search
```