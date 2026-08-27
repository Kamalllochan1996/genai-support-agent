from pydantic import BaseModel, Field


class ChatRequest(BaseModel):

    session_id: str = Field(
        min_length=1,
        max_length=100
    )

    question: str = Field(
        min_length=1,
        max_length=2000
    )


class Source(BaseModel):
    source: str
    page: int | None = None


class ChatResponse(BaseModel):
    answer: str
    sources: list[Source]