from app.ingestion.chunk import DocumentChunk
from app.ingestion.document import Document


class DocumentChunker:

    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
    ):
        if chunk_size <= 0:
            raise ValueError(
                "chunk_size must be greater than 0"
            )

        if chunk_overlap < 0:
            raise ValueError(
                "chunk_overlap cannot be negative"
            )

        if chunk_overlap >= chunk_size:
            raise ValueError(
                "chunk_overlap must be smaller "
                "than chunk_size"
            )

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split(
        self,
        document: Document,
    ) -> list[DocumentChunk]:

        content = document.content

        if not content.strip():
            return []

        chunks = []

        start = 0
        chunk_index = 0

        step = (
            self.chunk_size
            - self.chunk_overlap
        )

        while start < len(content):

            end = start + self.chunk_size

            chunk_text = content[start:end]

            chunks.append(
                DocumentChunk(
                    content=chunk_text,
                    source=document.source,
                    metadata={
                        **document.metadata,
                        "chunk_index": chunk_index,
                    },
                )
            )

            chunk_index += 1
            start += step

        return chunks