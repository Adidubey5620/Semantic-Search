import asyncio

from sqlalchemy import text

from app.database import SessionLocal
from app.embeddings.service import create_embedding


async def main():
    query = "How can text be converted into embeddings?"

    query_embedding = create_embedding(query)

    print(f"Query: {query}")
    print(f"Embedding dimensions: {len(query_embedding)}")

    async with SessionLocal() as session:

        # --------------------------------------------------
        # 1. Semantic search
        # --------------------------------------------------

        print("\nTop 5 semantic search results:\n")

        search_result = await session.execute(
            text("""
                SELECT
                    id,
                    content,
                    embedding <=> CAST(:embedding AS vector) AS distance
                FROM documents
                WHERE embedding IS NOT NULL
                ORDER BY embedding <=> CAST(:embedding AS vector)
                LIMIT 5
            """),
            {
                "embedding": str(query_embedding),
            }
        )

        rows = search_result.fetchall()

        for i, row in enumerate(rows, start=1):
            print(f"{i}. ID: {row.id}")
            print(f"   Distance: {row.distance:.4f}")
            print(f"   Content: {row.content}")
            print()

        # --------------------------------------------------
        # 2. Query execution plan
        # --------------------------------------------------

        print("\nQuery execution plan:\n")

        explain_result = await session.execute(
            text("""
                EXPLAIN (ANALYZE, BUFFERS)
                SELECT
                    id,
                    content,
                    embedding <=> CAST(:embedding AS vector) AS distance
                FROM documents
                WHERE embedding IS NOT NULL
                ORDER BY embedding <=> CAST(:embedding AS vector)
                LIMIT 5
            """),
            {
                "embedding": str(query_embedding),
            }
        )

        for row in explain_result:
            print(row[0])


if __name__ == "__main__":
    asyncio.run(main())