from app.api.services.llm_interface import LLMInterface


class FakeLLM(LLMInterface):

    def generate(
        self,
        prompt: str,
        request_id: str | None = None,
    ) -> str:

        return "This is a fake LLM response."


class FailingFakeLLM(LLMInterface):

    def generate(
        self,
        prompt: str,
        request_id: str | None = None,
    ) -> str:

        from app.api.exceptions import LLMServiceError

        raise LLMServiceError(
            "The LLM service is currently unavailable."
        )