from pydantic import BaseModel, Field


class DocumentCreate(BaseModel):
    content: str = Field(
        min_length=1,
        max_length=10000,
        description="Text content to index",
    )

    category: str | None = Field(
        default=None,
        max_length=100,
    )

    source: str | None = Field(
        default=None,
        max_length=255,
    )


class DocumentResponse(BaseModel):
    id: int
    content: str
    category: str | None
    source: str | None

    model_config = {
        "from_attributes": True,
    }


class SearchRequest(BaseModel):
    query: str = Field(
        min_length=1,
    )

    limit: int = Field(
        default=5,
        ge=1,
        le=50,
    )

    offset: int = Field(
        default=0,
        ge=0,
    )

    min_score: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
    )

    category: str | None = None

    source: str | None = None


class SearchResult(BaseModel):
    id: int
    content: str
    category: str | None = None
    source: str | None = None
    score: float

class SearchResponse(BaseModel):
    results: list[SearchResult]
    count: int
