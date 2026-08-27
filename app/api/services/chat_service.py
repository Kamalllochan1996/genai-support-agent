import logging

from app.api.exceptions import ChatServiceError
from app.rag.rag_service import RAGService


logger = logging.getLogger(__name__)


class ChatService:

    def __init__(
        self,
        rag_service: RAGService,
    ):
        self.rag_service = rag_service

    def generate_response(
        self,
        question: str,
        history: list[dict] | None = None,
        request_id: str | None = None,
    ) -> dict:

        logger.info(
            "Generating chat response | request_id=%s",
            request_id,
        )

        if not question.strip():

            logger.warning(
                "Empty question received | request_id=%s",
                request_id,
            )

            raise ChatServiceError(
                "Question cannot be empty."
            )

        if history is None:
            history = []

        result = self.rag_service.answer(
            question=question,
            history=history,
        )

        logger.info(
            "Chat response generation completed | request_id=%s",
            request_id,
        )

        return result