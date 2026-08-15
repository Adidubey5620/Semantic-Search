import asyncio

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from app.database import DATABASE_URL


async def test_connection():
    print("DATABASE URL:", DATABASE_URL.replace(
        DATABASE_URL.split("@")[0].split("//")[1],
        "***"
    ), flush=True)

    engine = create_async_engine(
        DATABASE_URL,
        pool_pre_ping=True,
        pool_size=1,
        max_overflow=0,
    )

    try:
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT 1"))
            print("SQLALCHEMY CONNECTION OK:", result.scalar(), flush=True)

    except Exception as e:
        print("SQLALCHEMY CONNECTION FAILED", flush=True)
        print(type(e).__name__, flush=True)
        print(e, flush=True)

    finally:
        await engine.dispose()


asyncio.run(test_connection())
