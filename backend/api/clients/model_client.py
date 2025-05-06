from api.config import Settings
from api.services.models.ollama import OllamaClient
from langchain_ollama import ChatOllama

# from api.services.models.openai import OpenAIClient


def get_model_client():
    """
    Fabrica el cliente adecuado según MODEL_BACKEND
    y le pasa el modelo desde la config.
    """
    cfg = Settings()

    if cfg.MODEL_BACKEND == "ollama":
        return ChatOllama(model=cfg.OLLAMA_MODEL)
        # return OllamaClient(base_url=cfg.OLLAMA_HOST, model=cfg.OLLAMA_MODEL)
    # elif cfg.MODEL_BACKEND == "openai":
    #     return OpenAIClient(api_key=cfg.OPENAI_KEY)
    else:
        raise ValueError(f"Backend desconocido: {cfg.MODEL_BACKEND}")
