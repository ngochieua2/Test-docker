import os
from typing import ClassVar, Dict, Any
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

# Load environment variables from .env file
env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path=env_path)


class Settings(BaseSettings):
    PROJECT_NAME: str = "Data Cooking APIs"
    API_V1_STR: str = "/api/v1"

    # Redis
    REDIS_HOST: str
    REDIS_PORT: int

    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI: str
    echo_sql: bool = True

    # OpenAI / ChatGPT
    CHAT_GPTs_API_KEY: str
    CHAT_GPTs_MODEL: str

    # Kafka
    KAFKA_BOOTSTRAP: str
    KAFKA_TOPIC: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    IMPORT_DATA_PROMPT : str 


# Global settings instance
settings = Settings()
