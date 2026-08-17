class DocumentNotFoundError(Exception):
    """Raised when a requested document does not exist."""

    def __init__(self, document_id: int):
        self.document_id = document_id
        super().__init__(
            f"Document with id {document_id} was not found."
        )


class EmbeddingGenerationError(Exception):
    """Raised when an embedding cannot be generated."""

    def __init__(self, message: str = "Failed to generate embedding."):
        self.message = message
        super().__init__(self.message)