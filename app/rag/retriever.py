from app.core.config import settings
from app.rag.embedding_service import EmbeddingService
from app.rag.vector_store import VectorStore


class Retriever:

    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.vector_store = VectorStore()

    def retrieve(self, question: str) -> list[dict]:

        query_embedding = (
            self.embedding_service.embed_text(question)
        )

        results = self.vector_store.search_with_scores(
            query_embedding,
            top_k=settings.TOP_K
        )

        relevant_results = [
            result
            for result in results
            if result["distance"] <= settings.MAX_DISTANCE
        ]

        return relevant_results