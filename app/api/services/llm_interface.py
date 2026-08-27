from abc import ABC, abstractmethod


class LLMInterface(ABC):

    @abstractmethod
    def generate(
        self,
        prompt: str,
        request_id: str | None = None,
    ) -> str:
        pass