from fastapi import Request
from fastapi.responses import JSONResponse

from app.api.exceptions import (
    ChatServiceError,
    LLMServiceError,
)


async def chat_service_exception_handler(
    request: Request,
    exc: ChatServiceError,
):
    return JSONResponse(
        status_code=500,
        content={
            "error": "Chat service error",
            "message": exc.message,
        },
    )


async def llm_service_exception_handler(
    request: Request,
    exc: LLMServiceError,
):
    return JSONResponse(
        status_code=503,
        content={
            "error": "LLM service unavailable",
            "message": exc.message,
        },
    )