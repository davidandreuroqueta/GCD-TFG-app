from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    FLASK_ENV: str = "development"
    API_KEY: str = "" 
    ASSITANT_ID: str = "default" 

    MODEL_BACKEND: str = "ollama"
    
    OLLAMA_MODEL: str         
    OLLAMA_HOST: str
    
    OPENAI_KEY: str = ""

    JWT_SECRET_KEY: str = ""

    PROMETHEUS_ENABLE: bool = False

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """
    Devuelve siempre la misma instancia de Settings,
    cargada una sola vez desde .env.
    """
    return Settings()