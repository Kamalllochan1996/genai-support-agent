from app.embedding.embedding_service import EmbeddingService
from app.retrieval.retrieval_result import RetrievedChunk
from app.vectorstore.chroma_store import ChromaVectorStore


class RetrievalService:

    def __init__(
        self,
        embedding_service: EmbeddingService,
        vector_store: ChromaVectorStore,
    ):
        self.embedding_service = embedding_service
        self.vector_store = vector_store

    def retrieve(
        self,
        query: str,
        top_k: int = 3,
        max_distance: float = 0.8,
    ) -> list[RetrievedChunk]:

        query_embedding = (
            self.embedding_service.embed_text(
                query
            )
        )

        results = self.vector_store.search(
            query_embedding=query_embedding,
            top_k=top_k,
        )

        retrieved_chunks = [
            RetrievedChunk(
                content=result["content"],
                metadata=result["metadata"],
                distance=result["distance"],
            )
            for result in results
        ]

        return [
            chunk
            for chunk in retrieved_chunks
            if chunk.distance <= max_distance
        ]