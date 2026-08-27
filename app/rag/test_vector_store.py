from app.rag.embedding_service import EmbeddingService
from app.rag.vector_store import VectorStore


embedding_service = EmbeddingService()
vector_store = VectorStore()


documents = [
    {
        "text": "Employees are entitled to 12 days of casual leave every year.",
        "metadata": {
            "source": "company_policy.pdf",
            "page": 2,
            "chunk_id": 0
        }
    },
    {
        "text": "Employees receive medical insurance benefits from the company.",
        "metadata": {
            "source": "company_policy.pdf",
            "page": 5,
            "chunk_id": 1
        }
    },
    {
        "text": "Employees must reset their password every 90 days.",
        "metadata": {
            "source": "security_policy.pdf",
            "page": 3,
            "chunk_id": 0
        }
    }
]


for document in documents:

    document["embedding"] = embedding_service.embed_text(
        document["text"]
    )


vector_store.add_documents(documents)


query = "How many casual leaves do employees get?"

query_embedding = embedding_service.embed_text(query)

results = vector_store.search(
    query_embedding,
    top_k=2
)


print(results)