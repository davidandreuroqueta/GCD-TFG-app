import requests
from api.services.models.base import BaseClient

class OllamaClient(BaseClient):
    def __init__(self, base_url: str, model: str = "llama2"):
        self.base_url = base_url.rstrip("/")
        self.model = model

    def predict(self, prompt: str, **kwargs) -> str:
        """
        Llama al endpoint /models/{model}/completions de Ollama.
        """
        url = f"{self.base_url}/api/generate"
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            **kwargs,
        }
        resp = requests.post(url, json=payload)
        resp.raise_for_status()
        data = resp.json()
        # Ajusta si tu versión de Ollama devuelve la respuesta en otro campo
        print(data)
        return data["response"]