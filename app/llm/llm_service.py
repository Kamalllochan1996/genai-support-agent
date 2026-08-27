import time

import ollama

from app.config import settings
from app.core.metrics import (
    llm_errors_total,
    llm_request_duration_seconds,
    llm_requests_total,
)


class LLMService:

    def __init__(self):

        self.model = settings.model_name

        self.client = ollama.Client(
            host="http://localhost:11434",
            timeout=60,
        )

    def generate(
        self,
        prompt: str,
    ) -> str:

        llm_requests_total.inc()

        start_time = time.perf_counter()

        try:

            response = self.client.chat(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
            )

            return response["message"]["content"]

        except Exception:

            llm_errors_total.inc()

            raise

        finally:

            duration = (
                time.perf_counter()
                - start_time
            )

            llm_request_duration_seconds.observe(
                duration
            )