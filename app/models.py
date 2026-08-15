from sqlalchemy import Column, BigInteger, Text
from app.database import Base
from app.embeddings import create_embedding

class Document(Base):
    __tablename__ = "documents"
    id = Column(BigInteger, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    embedding = Column(Text, nullable=False)