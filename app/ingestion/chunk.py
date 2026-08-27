from dataclasses import dataclass, field


@dataclass
class DocumentChunk:
    content: str
    source: str
    metadata: dict = field(
        default_factory=dict
    )
    embedding: list[float] | None = None