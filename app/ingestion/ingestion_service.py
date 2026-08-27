from pathlib import Path

from app.ingestion.chunk import DocumentChunk
from app.ingestion.chunker import DocumentChunker
from app.ingestion.loaders.loader_factory import (
    DocumentLoaderFactory,
)


class IngestionService:

    def __init__(
        self,
        chunker: DocumentChunker | None = None,
    ):
        self.chunker = (
            chunker
            if chunker is not None
            else DocumentChunker()
        )

    def ingest(
        self,
        file_path: Path,
    ) -> list[DocumentChunk]:

        loader = DocumentLoaderFactory.get_loader(
            file_path
        )

        document = loader.load(
            file_path
        )

        return self.chunker.split(
            document
        )