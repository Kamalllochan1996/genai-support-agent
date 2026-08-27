from abc import ABC, abstractmethod
from pathlib import Path

from app.ingestion.document import Document


class DocumentLoader(ABC):

    @abstractmethod
    def load(self, file_path: Path) -> Document:
        pass