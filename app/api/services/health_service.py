import logging

from app.api.services.health_status import HealthStatus
from app.api.services.llm_service import LLMService


logger = logging.getLogger(__name__)


class HealthService:

    def __init__(
        self,
        llm_service: LLMService,
    ):
        self.llm_service = llm_service

    def check_llm(self) -> HealthStatus:

        healthy = self.llm_service.health_check()

        if healthy:
            return HealthStatus(
                name="ollama",
                healthy=True,
                message="Ollama is available",
            )

        return HealthStatus(
            name="ollama",
            healthy=False,
            message="Ollama is unavailable",
        )

    def check_all(self) -> list[HealthStatus]:

        return [
            self.check_llm(),
        ]

    def is_ready(self) -> bool:

        statuses = self.check_all()

        return all(
            status.healthy
            for status in statuses
        )