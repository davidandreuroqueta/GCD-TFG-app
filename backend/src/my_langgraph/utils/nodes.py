import os
from dotenv import load_dotenv
from ollama import Client
from langchain_core.messages import SystemMessage, AIMessage, HumanMessage
from my_langgraph.utils.state import State

load_dotenv()

# model = os.getenv("OLLAMA_MODEL", "qwen3:4b")
# llm = ChatOllama(
#     model=model,
#     temperature=0,
# )

# Mensaje de sistema para el modelo
system_message = SystemMessage(content="Eres un asistente útil. Responde de manera concisa.")

def chat_node(state: State) -> dict:
    """
    Toma el estado, extrae los mensajes (que pueden ser objetos o dicts),
    los formatea para Ollama, ejecuta la llamada y devuelve el mensaje de IA.
    """
    ollama_messages = []

    for m in state["messages"]:
        # Determina role y content según el tipo
        if isinstance(m, SystemMessage):
            role = "system"
            content = m.content
        elif isinstance(m, HumanMessage):
            role = "user"
            content = m.content
        elif isinstance(m, AIMessage):
            role = "assistant"
            content = m.content
        elif isinstance(m, dict):
            # Manejo de dicts: caídas seguras con get()
            role = m.get("role", "user")
            content = m.get("content", "")
        else:
            # Fallback: convierte en string
            role = "user"
            content = str(m)

        ollama_messages.append({"role": role, "content": content})

    # Incluimos también el mensaje de sistema al inicio si lo quieres siempre
    ollama_messages.insert(0, {"role": "system", "content": system_message.content})

    # Llama al modelo local con la variable, no como string literal
    response = ollama_client.chat(model=MODEL_NAME, messages=ollama_messages)

    # Extrae el contenido de la respuesta
    content = response["message"]["content"]

    # Devuelve la respuesta empaquetada como AIMessage
    return {"messages": [AIMessage(content=content)]}