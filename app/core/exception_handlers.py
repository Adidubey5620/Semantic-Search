import logging

from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.exceptions import (
    DocumentNotFoundError,
    EmbeddingGenerationError,
)

logger = logging.getLogger(__name__)

async def document_not_found_exception_handler(
    request: Request,
    exc: DocumentNotFoundError,
):
    logger.warning(
        "Document not found",
        extra={
            "method": request.method,
            "path": request.url.path,
            "query": str(request.query_params),
            "document_id": exc.document_id,
        },
    )

    return JSONResponse(
        status_code=404,
        content={
            "detail": f"Document with id {exc.document_id} was not found."
        },
    )

async def embedding_generation_exception_handler(
    request: Request,
    exc: EmbeddingGenerationError
):
    logger.exception(
        "Embedding generation failed",
        extra={
            "method": request.method,
            "path": request.url.path,
            "query": request.query_params
        }
    )
    return JSONResponse(
        status_code=503,
        content={
            "detail": "Embedding generation failed. Please try again later."
        }
    )

async def general_exception_handler(
    request: Request,
    exc: Exception
):
    logger.exception("Unhandled application error",
    extra={
        "method": request.method,
        "path": request.url.path,
        "query": request.query_params
    },
    )
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error"
        }
    )