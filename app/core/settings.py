from pydantic_settings import BaseSettings
from app.core.settings import settings


class Settings(BaseSettings):

    OPENAI_API_KEY: str = ""

    CHROMA_DB_PATH: str = settings.CHROMA_DB_PATH

    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"

    TOP_K: int = 3

    MAX_DISTANCE: float = 1.5

    class Config:
        env_file = ".env"


settings = Settings()