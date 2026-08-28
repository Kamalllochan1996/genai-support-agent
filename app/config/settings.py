from typing import List, Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    app_name: str = Field(
        default="GenAI Support Agent API",
        min_length=1,
    )

    app_version: str = Field(
        default="1.0.0",
        min_length=1,
    )

    environment: Literal[
        "development",
        "testing",
        "staging",
        "production",
    ] = "development"

    debug: bool = False

    llm_provider: Literal[
        "ollama",
        "huggingface",
        "openai",
    ] = "ollama"

    model_name: str = Field(
        default="llama3.2:3b",
        min_length=1,
    )

    hf_token: str | None = None

    ollama_base_url: str = Field(
        default="http://localhost:11434",
        min_length=1,
    )

    cors_origins: List[str] = Field(
        default_factory=lambda: [
            "http://localhost:3000",
            "http://127.0.0.1:3000",
        ]
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()