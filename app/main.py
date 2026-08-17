from fastapi import FastAPI

from app.api.routes.documents import router as documents_router
from app.api.routes.health import router as health_router

from app.core.exception_handlers import (
    embedding_generation_exception_handler,
    general_exception_handler,
)

from app.core.exceptions import EmbeddingGenerationError
from app.core.logging import configure_logging

configure_logging()

app = FastAPI(
    title="Semantic Search API",
    version="1.0.0"
)

app.add_exception_handler(
    EmbeddingGenerationError,
    embedding_generation_exception_handler,
)
app.add_exception_handler(
    Exception, 
    general_exception_handler
)


app.include_router(documents_router)
app.include_router(health_router)


@app.get("/")
async def root():
    return {
        "message": "Semantic Search API is running"
    }