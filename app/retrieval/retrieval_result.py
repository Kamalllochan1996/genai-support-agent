from dataclasses import dataclass, field


@dataclass
class RetrievedChunk:
    content: str
    metadata: dict = field(
        default_factory=dict
    )
    distance: float = 0.0