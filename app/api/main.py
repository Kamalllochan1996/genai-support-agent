import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

from app.api.exception_handlers import (
    chat_service_exception_handler,
    llm_service_exception_handler,
)
from app.api.exceptions import (
    ChatServiceError,
    LLMServiceError,
)
from app.api.middleware import (
    request_logging_middleware,
)
from app.api.routes.background import (
    router as background_router,
)
from app.api.routes.chat import router as chat_router
from app.api.routes.health import router as health_router
from app.config import settings
from app.core.logging_config import setup_logging


setup_logging()

logger = logging.getLogger(__name__)


app = FastAPI(
    title=settings.app_name,
    description="Backend API for the GenAI Support Agent",
    version=settings.app_version,
    debug=settings.debug,
)


Instrumentator().instrument(app).expose(app)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.middleware("http")(
    request_logging_middleware
)


app.add_exception_handler(
    ChatServiceError,
    chat_service_exception_handler,
)

app.add_exception_handler(
    LLMServiceError,
    llm_service_exception_handler,
)


@app.get("/")
def root():

    logger.info("Root endpoint called")

    return {
        "message": f"{settings.app_name} is running"
    }


app.include_router(
    background_router,
)

app.include_router(
    chat_router,
    prefix="/api/v1",
)

app.include_router(
    health_router,
    prefix="/api/v1",
)