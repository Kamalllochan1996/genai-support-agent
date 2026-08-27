from pathlib import Path

from app.ingestion.loaders.base import DocumentLoader
from app.ingestion.loaders.pdf_loader import PDFLoader
from app.ingestion.loaders.text_loader import TextLoader


class DocumentLoaderFactory:

    @staticmethod
    def get_loader(
        file_path: Path,
    ) -> DocumentLoader:

        extension = file_path.suffix.lower()

        if extension == ".pdf":
            return PDFLoader()

        if extension == ".txt":
            return TextLoader()

        raise ValueError(
            f"Unsupported file type: {extension}"
        )