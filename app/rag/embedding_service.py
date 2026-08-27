from sentence_transformers import SentenceTransformer


class EmbeddingService:

    def __init__(self):
        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

    def embed_text(self, text: str) -> list[float]:
        embedding = self.model.encode(text)

        return embedding.tolist()

    def embed_documents(
        self,
        documents: list[dict]
    ) -> list[dict]:

        results = []

        for document in documents:

            embedding = self.embed_text(
                document["text"]
            )

            results.append({
                "text": document["text"],
                "metadata": document["metadata"],
                "embedding": embedding
            })

        return results