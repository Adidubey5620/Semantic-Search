from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

from app.core.config import settings

DATABASE_URL = settings.database_url

DATABASE_URL = DATABASE_URL.replace(
        "postgresql://",
        "postgresql+asyncpg://"
)

#  Create the SQLAlchemy engine
engine = create_async_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=1,
    max_overflow=0,
)

#  Create database session factory
SessionLocal = async_sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
)

#  Base class for all models
Base = declarative_base()

async def get_db():
    db: AsyncSession = SessionLocal()
    try: 
        yield db
    finally:
        await db.close()

async def close_database():
    await engine.dispose()