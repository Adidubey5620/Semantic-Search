from app.services.document_service import (
    search_documents,
    create_document
)
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.core.exceptions import EmbeddingGenerationError
from app.models import Document

@pytest.mark.asyncio
async def test_create_document_success():
    db = MagicMock()

    db.commit = AsyncMock()
    db.refresh = AsyncMock()
    db.rollback = AsyncMock()
    db.execute = AsyncMock()

    fake_embedding = [0.1, 0.2, 0.3]

    async def fake_refresh(document):
        document.id = 1

    db.refresh.side_effect = fake_refresh

    with patch(
        "app.services.document_service.create_embedding",
        return_value=fake_embedding,
    ) as mock_create_embedding:

        document = await create_document(
            db=db,
            content="FastAPI semantic search",
            category="technology",
            source="test",
        )

    mock_create_embedding.assert_called_once_with(
        "FastAPI semantic search"
    )

    db.add.assert_called_once()
    db.commit.assert_awaited_once()
    db.refresh.assert_awaited_once()

    assert isinstance(document, Document)
    assert document.id == 1
    assert document.content == "FastAPI semantic search"
    assert document.category == "technology"
    assert document.source == "test"
    assert document.embedding == fake_embedding


@pytest.mark.asyncio
async def test_create_document_embedding_failure():
    db = MagicMock()

    db.commit = AsyncMock()
    db.refresh = AsyncMock()
    db.rollback = AsyncMock()

    with patch(
        "app.services.document_service.create_embedding",
        side_effect=RuntimeError("Embedding service failed"),
    ):

        with pytest.raises(EmbeddingGenerationError):
            await create_document(
                db=db,
                content="This should fail",
                category="technology",
                source="test",
            )

    db.add.assert_not_called()
    db.commit.assert_not_awaited()
    db.refresh.assert_not_awaited()
    db.rollback.assert_not_awaited()

@pytest.mark.asyncio
async def test_create_document_database_failure_rolls_back():
    db = MagicMock()

    db.commit = AsyncMock(
        side_effect=RuntimeError("Database commit failed")
    )
    db.refresh = AsyncMock()
    db.rollback = AsyncMock()

    fake_embedding = [0.1, 0.2, 0.3]

    with patch(
        "app.services.document_service.create_embedding",
        return_value=fake_embedding,
    ):

        with pytest.raises(RuntimeError, match="Database commit failed"):
            await create_document(
                db=db,
                content="Database failure test",
                category="technology",
                source="test",
            )

    db.add.assert_called_once()

    db.commit.assert_awaited_once()

    db.rollback.assert_awaited_once()

    db.refresh.assert_not_awaited()

@pytest.mark.asyncio
async def test_search_documents_returns_results():
    db = MagicMock()

    db.execute = AsyncMock()

    fake_embedding = [0.1, 0.2, 0.3]

    hnsw_result = MagicMock()

    search_result = MagicMock()

    search_result.all.return_value = [
        MagicMock(
            id=1,
            content="FastAPI semantic search",
            category="technology",
            source="test",
            score=0.92,
        ),
        MagicMock(
            id=2,
            content="Python programming",
            category="technology",
            source="blog",
            score=0.85,
        ),
    ]

    db.execute.side_effect = [
        hnsw_result,
        search_result,
    ]

    with patch(
        "app.services.document_service.create_embedding",
        return_value=fake_embedding,
    ) as mock_create_embedding:

        result = await search_documents(
            db=db,
            query="Python programming",
            limit=5,
            offset=0,
            min_score=0.8,
        )

    mock_create_embedding.assert_called_once_with(
        "Python programming"
    )

    assert result["count"] == 2
    assert len(result["results"]) == 2

    assert result["results"][0]["id"] == 1
    assert result["results"][0]["content"] == "FastAPI semantic search"
    assert result["results"][0]["score"] == 0.92

    assert result["results"][1]["id"] == 2
    assert result["results"][1]["content"] == "Python programming"
    assert result["results"][1]["score"] == 0.85

    assert db.execute.await_count == 2

@pytest.mark.asyncio
async def test_search_documents_returns_empty_results():
    db = MagicMock()

    db.execute = AsyncMock()

    fake_embedding = [0.1, 0.2, 0.3]

    hnsw_result = MagicMock()

    search_result = MagicMock()
    search_result.all.return_value = []

    db.execute.side_effect = [
        hnsw_result,
        search_result,
    ]

    with patch(
        "app.services.document_service.create_embedding",
        return_value=fake_embedding,
    ):

        result = await search_documents(
            db=db,
            query="quantum mechanics",
            limit=5,
            offset=0,
            min_score=0.95,
        )

    assert result == {
        "results": [],
        "count": 0,
    }

    assert db.execute.await_count == 2

@pytest.mark.asyncio
async def test_search_documents_with_filters_and_pagination():
    db = MagicMock()

    db.execute = AsyncMock()

    fake_embedding = [0.1, 0.2, 0.3]

    hnsw_result = MagicMock()

    search_result = MagicMock()

    search_result.all.return_value = [
        MagicMock(
            id=5,
            content="FastAPI semantic search",
            category="technology",
            source="documentation",
            score=0.91,
        ),
    ]

    db.execute.side_effect = [
        hnsw_result,
        search_result,
    ]

    with patch(
        "app.services.document_service.create_embedding",
        return_value=fake_embedding,
    ):

        result = await search_documents(
            db=db,
            query="semantic search",
            limit=2,
            offset=4,
            min_score=0.85,
            category="technology",
            source="documentation",
        )

    assert result["count"] == 1
    assert result["results"][0]["id"] == 5
    assert result["results"][0]["score"] == 0.91

    assert db.execute.await_count == 2