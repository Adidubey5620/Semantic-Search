import pytest
from httpx import ASGITransport, AsyncClient
from unittest.mock import patch

from app.main import app
from app.core.exceptions import EmbeddingGenerationError

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