from pathlib import Path

from pypdf import PdfReader

from app.ingestion.document import Document
from app.ingestion.loaders.base import DocumentLoader


class PDFLoader(DocumentLoader):

    def load(self, file_path: Path) -> Document:

        reader = PdfReader(file_path)

        pages = []

        for page_number, page in enumerate(
            reader.pages,
            start=1,
        ):
            text = page.extract_text()

            if text:
                pages.append(
                    f"[Page {page_number}]\n{text}"
                )

        content = "\n\n".join(pages)

        return Document.from_file(
            file_path=file_path,
            content=content,
        )