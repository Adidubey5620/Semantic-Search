from app.schemas import SearchResponse
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas import (
    DocumentCreate,
    DocumentResponse,
    SearchRequest,
    SearchResult,
)
from app.services.document_service import (
    create_document as create_document_service,
    get_documents as get_documents_service,
    search_documents as search_documents_service,
)


router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=DocumentResponse,
)
async def create_document_route(
    document: DocumentCreate,
    db: AsyncSession = Depends(get_db),
):
    return await create_document_service(
        db=db,
        content=document.content,
        category=document.category,
        source=document.source,
    )


@router.get(
    "/",
    response_model=list[DocumentResponse],
)
async def get_documents_route(
    db: AsyncSession = Depends(get_db),
):
    return await get_documents_service(db)


@router.post(
    "/search",
    status_code=status.HTTP_200_OK,
    response_model=SearchResponse,
)
async def search_documents_route(
    request: SearchRequest,
    db: AsyncSession = Depends(get_db),
):
    return await search_documents_service(
        db=db,
        query=request.query,
        limit=request.limit,
        offset=request.offset,
        min_score=request.min_score,
        category=request.category,
        source=request.source,
    )