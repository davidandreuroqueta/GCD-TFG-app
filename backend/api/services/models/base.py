from abc import ABC, abstractmethod


class BaseClient(ABC):
    """
    Interfaz base para todos los clientes de LLM.
    """

    @abstractmethod
    def predict(self, prompt: str, **kwargs) -> str:
        """
        Envía el prompt al modelo y devuelve la respuesta como texto.
        """
        ...