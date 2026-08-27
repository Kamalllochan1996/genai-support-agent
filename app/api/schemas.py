from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str


class ChatRequest(BaseModel):
    question: str
    history: list[dict] = Field(
        default_factory=list
    )


class ChatSource(BaseModel):
    source: str | None = None
    page: int | None = None


class ChatResponse(BaseModel):
    question: str
    answer: str
    sources: list[ChatSource] = Field(
        default_factory=list
    )