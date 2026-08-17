import pytest
from httpx import ASGITransport, AsyncClient
from unittest.mock import patch

from app.main import app
from app.core.exceptions import EmbeddingGenerationError


@pytest.mark.asyncio
async def test_health_check():
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:
        response = await client.get("/health/")

    assert response.status_code == 200

    assert response.json() == {
        "status": "ok",
        "database": "ok",
    }


@pytest.mark.asyncio
async def test_get_documents():
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:
        response = await client.get("/documents/")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

    for document in data:
        assert "id" in document
        assert "content" in document
        assert "category" in document
        assert "source" in document

@pytest.mark.asyncio
async def test_create_document():
    transport = ASGITransport(app=app)

    payload = {
        "content": "Integration test document for semantic search.",
        "category": "test",
        "source": "pytest",
    }

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:
        response = await client.post(
            "/documents/",
            json=payload,
        )

    assert response.status_code == 201

    data = response.json()

    assert isinstance(data["id"], int)
    assert data["content"] == payload["content"]
    assert data["category"] == payload["category"]
    assert data["source"] == payload["source"]

@pytest.mark.asyncio
async def test_semantic_search():
    transport = ASGITransport(app=app)

    payload = {
        "query": "FastAPI semantic search",
        "limit": 5,
        "offset": 0,
        "min_score": 0.0,
    }

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:
        response = await client.post(
            "/documents/search",
            json=payload,
        )

    assert response.status_code == 200

    data = response.json()

    assert "results" in data
    assert "count" in data

    assert isinstance(data["results"], list)
    assert isinstance(data["count"], int)

    for result in data["results"]:
        assert "id" in result
        assert "content" in result
        assert "category" in result
        assert "source" in result
        assert "score" in result

        assert 0.0 <= result["score"] <= 1.0

@pytest.mark.asyncio
async def test_create_document_embedding_failure():
    transport = ASGITransport(app=app)

    payload = {
        "content": "This document should trigger an embedding failure.",
        "category": "test",
        "source": "pytest",
    }

    with patch(
        "app.services.document_service.create_embedding",
        side_effect=EmbeddingGenerationError(),
    ):
        async with AsyncClient(
            transport=transport,
            base_url="http://test",
        ) as client:
            response = await client.post(
                "/documents/",
                json=payload,
            )

    assert response.status_code == 503

    assert response.json() == {
        "detail": "Embedding generation failed. Please try again later."
    }