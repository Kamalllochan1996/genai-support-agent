from app.api.services.chat_service import ChatService
from app.api.services.llm_service import LLMService
from app.rag.rag_service import RAGService


def get_llm_service() -> LLMService:
    return LLMService()


def get_rag_service() -> RAGService:
    return RAGService()


def get_chat_service() -> ChatService:
    return ChatService(
        rag_service=get_rag_service(),
    )