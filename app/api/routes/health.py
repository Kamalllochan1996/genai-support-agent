import logging

from fastapi import APIRouter, Depends

from app.api.dependencies import get_llm_service
from app.api.services.llm_service import LLMService


logger = logging.getLogger(__name__)


router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


@router.get("")
def health_check():

    return {
        "status": "healthy",
    }


@router.get("/llm")
def llm_health_check(
    llm_service: LLMService = Depends(
        get_llm_service
    ),
):

    is_healthy = llm_service.health_check()

    if is_healthy:

        return {
            "status": "healthy",
            "llm_provider": "ollama",
        }

    return {
        "status": "unhealthy",
        "llm_provider": "ollama",
    }