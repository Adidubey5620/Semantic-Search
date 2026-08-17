import logging

from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.exceptions import EmbeddingGenerationError
from app.embeddings.service import create_embedding
from app.models import Document


logger = logging.getLogger(__name__)


async def create_document(
    db: AsyncSession,
    content: str,
    category: str | None = None,
    source: str | None = None,
) -> Document:
    try:
        embedding = create_embedding(content)

    except Exception as exc:
        logger.exception(
            "Failed to generate document embedding"
        )

        raise EmbeddingGenerationError() from exc

    new_document = Document(
        content=content,
        category=category,
        source=source,
        embedding=embedding,
    )

    try:
        db.add(new_document)

        await db.commit()
        await db.refresh(new_document)

        logger.info(
            "Document created successfully: id=%s",
            new_document.id,
        )

        return new_document

    except Exception:
        await db.rollback()

        logger.exception(
            "Failed to create document"
        )

        raise


async def get_documents(
    db: AsyncSession,
) -> list[Document]:
    result = await db.execute(
        select(Document).order_by(Document.id)
    )

    return list(result.scalars().all())


async def search_documents(
    db: AsyncSession,
    query: str,
    limit: int,
    offset: int = 0,
    min_score: float = 0.0,
    category: str | None = None,
    source: str | None = None,
):
    try:
        query_embedding = create_embedding(query)

    except Exception as exc:
        logger.exception(
            "Failed to generate query embedding"
        )

        raise EmbeddingGenerationError() from exc

    distance = Document.embedding.cosine_distance(
        query_embedding
    )

    score = (1 - distance).label("score")

    conditions = [
        Document.embedding.is_not(None),
        score >= min_score,
    ]

    if category is not None:
        conditions.append(
            Document.category == category
        )

    if source is not None:
        conditions.append(
            Document.source == source
        )

    stmt = (
        select(
            Document.id,
            Document.content,
            Document.category,
            Document.source,
            score,
        )
        .where(*conditions)
        .order_by(distance)
        .offset(offset)
        .limit(limit)
    )

    await db.execute(
        text(
            f"SET hnsw.ef_search = {settings.hnsw_ef_search}"
        )
    )

    result = await db.execute(stmt)

    rows = result.all()

    documents = [
        {
            "id": row.id,
            "content": row.content,
            "category": row.category,
            "source": row.source,
            "score": float(row.score),
        }
        for row in rows
    ]

    count = len(documents)

    if count == 0:
        logger.info(
            "Semantic search returned no results: query=%r "
            "offset=%d limit=%d min_score=%f category=%r source=%r",
            query,
            offset,
            limit,
            min_score,
            category,
            source,
        )

    else:
        logger.info(
            "Semantic search completed: query=%r "
            "offset=%d limit=%d results=%d",
            query,
            offset,
            limit,
            count,
        )

    return {
        "results": documents,
        "count": count,
    }