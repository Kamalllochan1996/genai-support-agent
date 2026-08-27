from app.rag.embedding_service import EmbeddingService


embedding_service = EmbeddingService()

text = "Employees are entitled to 12 days of casual leave every year."

embedding = embedding_service.embed_text(text)

print("Embedding dimensions:", len(embedding))
print("First 10 values:", embedding[:10])