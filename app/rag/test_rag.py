from app.api.services.llm_service import LLMService
from app.embedding.embedding_service import EmbeddingService
from app.rag.context_builder import ContextBuilder
from app.rag.prompt_builder import RAGPromptBuilder
from app.rag.rag_service import RAGService
from app.retrieval.retrieval_service import RetrievalService
from app.vectorstore.chroma_store import ChromaVectorStore


embedding_service = EmbeddingService()

vector_store = ChromaVectorStore()

retrieval_service = RetrievalService(
    embedding_service=embedding_service,
    vector_store=vector_store,
)

rag_service = RAGService(
    retrieval_service=retrieval_service,
    llm_service=LLMService(),
    context_builder=ContextBuilder(),
    prompt_builder=RAGPromptBuilder(),
)

answer = rag_service.answer(
    "How many casual leaves can an employee take?"
)

print("\nANSWER:")
print(answer)