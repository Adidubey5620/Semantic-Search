from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Document
from app.database import get_db
from app.schemas import DocumentResponse, DocumentCreate

router = APIRouter(
    prefix="/documents",
    tags = ["Documents"]
)

@router.post("/", response_model=DocumentResponse)
async def create_document(
    document: DocumentCreate,
    db: AsyncSession = Depends(get_db)
):
    new_document = Document(
        content=document.content
    )

    db.add(new_document)
    await db.commit()
    await db.refresh(new_document)

    return new_document


@router.get("/", response_model=list[DocumentResponse])
async def get_documents(
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Document)
    )
    document = result.scalars().all()
    
    return document


