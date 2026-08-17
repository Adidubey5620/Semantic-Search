import pytest
from pydantic import ValidationError

from app.schemas import (
    DocumentCreate,
    SearchRequest,
    SearchResponse,
)


def test_document_create_with_valid_data():
    document = DocumentCreate(
        content="Python is a programming language.",
        category="technology",
        source="test",
    )

    assert document.content == "Python is a programming language."
    assert document.category == "technology"
    assert document.source == "test"


def test_document_create_rejects_empty_content():
    with pytest.raises(ValidationError):
        DocumentCreate(content="")


def test_document_create_allows_optional_metadata():
    document = DocumentCreate(
        content="Some document content."
    )

    assert document.category is None
    assert document.source is None


def test_search_request_defaults():
    request = SearchRequest(
        query="python"
    )

    assert request.limit == 5
    assert request.offset == 0
    assert request.min_score == 0.0
    assert request.category is None
    assert request.source is None


def test_search_request_accepts_valid_parameters():
    request = SearchRequest(
        query="machine learning",
        limit=10,
        offset=20,
        min_score=0.75,
        category="technology",
        source="blog",
    )

    assert request.query == "machine learning"
    assert request.limit == 10
    assert request.offset == 20
    assert request.min_score == 0.75
    assert request.category == "technology"
    assert request.source == "blog"


def test_search_request_rejects_invalid_limit():
    with pytest.raises(ValidationError):
        SearchRequest(
            query="python",
            limit=0,
        )

    with pytest.raises(ValidationError):
        SearchRequest(
            query="python",
            limit=51,
        )


def test_search_request_rejects_invalid_offset():
    with pytest.raises(ValidationError):
        SearchRequest(
            query="python",
            offset=-1,
        )


def test_search_request_rejects_invalid_min_score():
    with pytest.raises(ValidationError):
        SearchRequest(
            query="python",
            min_score=-0.1,
        )

    with pytest.raises(ValidationError):
        SearchRequest(
            query="python",
            min_score=1.1,
        )


def test_search_response_empty_results():
    response = SearchResponse(
        results=[],
        count=0,
    )

    assert response.results == []
    assert response.count == 0