import logging

from openai import OpenAI

from app.api.exceptions import LLMServiceError
from app.config import settings

try:
    from ollama import chat as ollama_chat
except ImportError:  # pragma: no cover
    ollama_chat = None


logger = logging.getLogger(__name__)


class LLMService:

    def __init__(self):
        self.client = None
        self.ollama_model = self._resolve_ollama_model()

        if settings.openai_api_key:
            self.client = OpenAI(
                api_key=settings.openai_api_key
            )
            logger.info("Using OpenAI provider for LLM generation")
            return

        logger.info(
            "No OpenAI key configured; using Ollama local model: %s",
            self.ollama_model,
        )

    def _resolve_ollama_model(self) -> str:
        configured = getattr(settings, "model_name", "") or ""
        if configured and ("/" not in configured and ":" in configured):
            return configured
        if configured and "/" in configured:
            return "llama3.2:3b"
        return "llama3.2:3b"

    def generate(
        self,
        prompt: str,
        request_id: str | None = None,
    ) -> str:

        logger.info(
            "LLM generation started | request_id=%s",
            request_id,
        )

        try:
            if self.client is not None:
                response = self.client.responses.create(
                    model=settings.model_name,
                    input=prompt,
                )
                answer = response.output_text
            elif ollama_chat is not None:
                response = ollama_chat(
                    model=self.ollama_model,
                    messages=[
                        {
                            "role": "user",
                            "content": prompt,
                        }
                    ],
                )
                answer = response["message"]["content"]
            else:
                raise LLMServiceError(
                    "No LLM provider is configured. Set OPENAI_API_KEY or ensure Ollama is available."
                )

            logger.info(
                "LLM generation completed | request_id=%s",
                request_id,
            )

            return answer

        except Exception as exc:

            logger.exception(
                "LLM provider failed | request_id=%s",
                request_id,
            )

            raise LLMServiceError(
                "The LLM service is currently unavailable."
            ) from exc