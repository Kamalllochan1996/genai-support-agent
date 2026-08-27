import os

from dotenv import load_dotenv


load_dotenv()


class Settings:

    APP_NAME = os.getenv(
        "APP_NAME",
        "GenAI Support Agent"
    )

    APP_VERSION = os.getenv(
        "APP_VERSION",
        "1.0.0"
    )

    CHROMA_PATH = os.getenv(
        "CHROMA_PATH",
        "chroma_db"
    )

    TOP_K = int(
        os.getenv("TOP_K", "3")
    )

    MAX_DISTANCE = float(
        os.getenv("MAX_DISTANCE", "1.5")
    )


settings = Settings()