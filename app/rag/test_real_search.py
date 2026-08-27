from app.rag.embedding_service import EmbeddingService
from app.rag.vector_store import VectorStore


embedding_service = EmbeddingService()
vector_store = VectorStore()


query = "How many casual leaves can an employee take?"

query_embedding = embedding_service.embed_text(
    query
)

results = vector_store.search(
    query_embedding,
    top_k=3
)


for i in range(len(results["documents"][0])):

    print("=" * 60)

    print("Result:", i + 1)

    print("Text:")
    print(results["documents"][0][i])

    print("\nMetadata:")
    print(results["metadatas"][0][i])

    print("\nDistance:")
    print(results["distances"][0][i])