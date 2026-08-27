from fastapi import FastAPI, HTTPException
from fastapi.middleware import Middleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from pydantic import BaseModel

from app.rag.rag_service import RAGService
from app.memory.session_manager import SessionManager
from app.schemas.chat import ChatRequest, ChatResponse
from app.core.logger import logger
from prometheus_fastapi_instrumentator import Instrumentator

from app.db.init_db import init_db
from app.config import settings

app = FastAPI(
    title=settings.app_name,
    description="Backend API for the GenAI Support Agent",
    version=settings.app_version,
    debug=settings.debug,
)

Instrumentator().instrument(app).expose(app)

rag = RAGService()
session_manager = SessionManager()


@app.middleware("http")
async def security_headers(request, call_next):

    response = await call_next(request)

    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"

    return response


@app.get("/")
def health_check():
    return {
        "status": "ok",
        "message": "GenAI Support Agent is running",
    }


@app.post(
    "/chat",
    response_model=ChatResponse,
)
def chat(request: ChatRequest):

    try:

        logger.info(
            "Chat request received | session_id=%s",
            request.session_id,
        )

        conversation = session_manager.get_session(
            request.session_id
        )

        result = rag.answer(
            request.question,
            conversation.get_history(),
        )

        conversation.add_user_message(
            request.question,
        )

        conversation.add_assistant_message(
            result["answer"],
        )

        logger.info(
            "Chat request completed | session_id=%s",
            request.session_id,
        )

        return result

    except Exception:

        logger.exception(
            "Chat request failed | session_id=%s",
            request.session_id,
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "An internal error occurred "
                "while processing the request."
            ),
        )