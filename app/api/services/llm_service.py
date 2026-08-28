import logging

from openai import OpenAI
from huggingface_hub import InferenceClient

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
        self.hf_client = None

        provider = settings.llm_provider.lower()

        if provider == "openai":

            if not settings.openai_api_key:
                raise LLMServiceError(
                    "OPENAI_API_KEY is required when using OpenAI."
                )

            self.client = OpenAI(
                api_key=settings.openai_api_key
            )

            logger.info(
                "Using OpenAI provider for LLM generation"
            )

        elif provider == "huggingface":

            if not settings.hf_token:
                raise LLMServiceError(
                    "HF_TOKEN is required when using Hugging Face."
                )

            self.hf_client = InferenceClient(
                token=settings.hf_token
            )

            logger.info(
                "Using Hugging Face provider for LLM generation"
            )

        elif provider == "ollama":

            self.ollama_model = self._resolve_ollama_model()

            logger.info(
                "Using Ollama local model: %s",
                self.ollama_model,
            )

        else:

            raise LLMServiceError(
                f"Unsupported LLM provider: {provider}"
            )

        self.provider = provider

    def _resolve_ollama_model(self) -> str:

        configured = (
            getattr(settings, "model_name", "")
            or ""
        )

        if configured and (
            "/" not in configured
            and ":" in configured
        ):
            return configured

        return "llama3.2:3b"

    def _resolve_huggingface_model(self) -> str:

        configured = (
            getattr(settings, "model_name", "")
            or ""
        )

        if configured and "/" in configured:
            return configured

        return "meta-llama/Llama-3.2-3B-Instruct"

    def generate(
        self,
        prompt: str,
        request_id: str | None = None,
    ) -> str:

        logger.info(
            "LLM generation started | request_id=%s | provider=%s",
            request_id,
            self.provider,
        )

        try:

            if self.provider == "openai":

                response = self.client.responses.create(
                    model=settings.model_name,
                    input=prompt,
                )

                answer = response.output_text

            elif self.provider == "huggingface":

                model = self._resolve_huggingface_model()

                response = self.hf_client.chat.completions.create(
                    model=model,
                    messages=[
                        {
                            "role": "user",
                            "content": prompt,
                        }
                    ],
                    max_tokens=512,
                )

                answer = response.choices[0].message.content

            elif self.provider == "ollama":

                if ollama_chat is None:
                    raise LLMServiceError(
                        "Ollama package is not installed."
                    )

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
                    "No supported LLM provider configured."
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