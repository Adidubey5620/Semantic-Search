from sqlalchemy import Column, Integer, String, Text
from pgvector.sqlalchemy import Vector

from app.database import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    content = Column(
        Text,
        nullable=False,
    )

    category = Column(
        String(100),
        nullable=True,
        index=True,
    )

    source = Column(
        String(255),
        nullable=True,
        index=True,
    )

    embedding = Column(
        Vector(384),
        nullable=True,
    )