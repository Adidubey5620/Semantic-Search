from pydantic import BaseModel

class DocumentCreate(BaseModel):
    content: str

class DocumentResponse(BaseModel):
    id: int
    content: str

    model_config = {
        "from_attributes": True
    }