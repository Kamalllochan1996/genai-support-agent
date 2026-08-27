from pathlib import Path

from app.ingestion.document import Document
from app.ingestion.loaders.base import DocumentLoader


class TextLoader(DocumentLoader):

    def load(self, file_path: Path) -> Document:

        content = file_path.read_text(
            encoding="utf-8"
        )

        return Document.from_file(
            file_path=file_path,
            content=content,
        )