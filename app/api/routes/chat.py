import logging

from fastapi import APIRouter, Depends, Request
from app.core.metrics import chat_requests_total

from app.api.dependencies import get_chat_service
from app.api.schemas import (
    ChatRequest,
    ChatResponse,
)
from app.api.services.chat_service import ChatService


logger = logging.getLogger(__name__)


router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post(
    "",
    response_model=ChatResponse,
)
def chat(
    request: Request,
    chat_request: ChatRequest,
    chat_service: ChatService = Depends(
        get_chat_service
    ),
):

    request_id = request.state.request_id

    logger.info(
        "Chat request received | request_id=%s",
        request_id,
    )

    result = chat_service.generate_response(
        question=chat_request.question,
        history=chat_request.history,
        request_id=request_id,
    )

    logger.info(
        "Chat response generated successfully | request_id=%s",
        request_id,
    )

    return ChatResponse(
        question=chat_request.question,
        answer=result["answer"],
        sources=result.get("sources", []),
    )