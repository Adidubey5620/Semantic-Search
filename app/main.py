from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.database import Base, engine
from app.routes import router
from app.models import Document  # Ensure models are loaded so they are registered with Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(
    title="Semantic Search API",
    lifespan=lifespan
)


app.include_router(router)


@app.get("/")
async def root():
    return {
        "message": "Semantic Search API is running"
    }