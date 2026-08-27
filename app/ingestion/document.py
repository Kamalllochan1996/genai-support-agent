from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Document:
    content: str
    source: str
    metadata: dict = field(
        default_factory=dict
    )
    page: int | None = None

    @classmethod
    def from_file(
        cls,
        file_path: Path,
        content: str,
        page: int | None = None,
    ) -> "Document":

        return cls(
            content=content,
            source=file_path.name,
            metadata={
                "file_path": str(file_path),
                "file_name": file_path.name,
                "file_type": file_path.suffix.lower(),
                "page": page,
            },
            page=page,
        )