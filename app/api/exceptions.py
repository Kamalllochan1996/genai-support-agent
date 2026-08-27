class ChatServiceError(Exception):
    """Base exception for chat service errors."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class LLMServiceError(Exception):
    """Raised when the LLM provider fails."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)