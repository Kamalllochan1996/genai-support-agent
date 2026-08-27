from app.embedding.embedding_service import EmbeddingService
from app.ingestion.chunk import DocumentChunk


class EmbeddingPipeline:

    def __init__(
        self,
        embedding_service: EmbeddingService,
    ):
        self.embedding_service = embedding_service

    def embed_chunks(
        self,
        chunks: list[DocumentChunk],
    ) -> list[DocumentChunk]:

        if not chunks:
            return []

        texts = [
            chunk.content
            for chunk in chunks
        ]

        vectors = (
            self.embedding_service.embed_documents(
                texts
            )
        )

        for chunk, vector in zip(
            chunks,
            vectors,
        ):
            chunk.embedding = vector

        return chunks