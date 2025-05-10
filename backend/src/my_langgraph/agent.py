from typing import Literal
from langchain_core.messages import BaseMessage
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, create_react_agent
from my_langgraph.utils.state import State
from my_langgraph.utils.nodes import chat_node
from my_langgraph.utils.tools import multiply


def build_graph():
    graph_builder = StateGraph(State)

    # Nodo de chat
    graph_builder.add_node("chat", chat_node)

    # Nodo de herramienta
    tool_node = ToolNode([multiply])
    graph_builder.add_node("multiply", tool_node)

    # Aristas de inicio
    graph_builder.add_edge(START, "chat")

    # Ruta condicional: si el modelo solicitó un tool, lo ejecuta
    def router(state: State, **kwargs):
        """
        Ejemplo de router que revisa si hay mensajes previos
        antes de extraer tool_calls.
        """
        # Comprueba que el state tenga al menos un item
        if state and len(state) > 0:
            print(state)
            last = state[-1]
            calls = last.additional_kwargs.get("tool_calls", [])
        else:
            # Si no hay nada, no hay llamadas a herramientas
            calls = []

        # Aquí sigue tu lógica de ruteo usando `calls`
        if calls:
            # …procesa tool calls…
            return {"next_node": "tool_node", "calls": calls}
        else:
            # …o continúa con chat…
            return {"next_node": "chat", "input": kwargs.get("input")}

    graph_builder.add_conditional_edges("chat", router)
    graph_builder.add_edge("multiply", END)

    return graph_builder.compile()

graph = build_graph()

from langchain_ollama import ChatOllama
import os
from langchain_experimental.tools.python.tool import PythonAstREPLTool
from langgraph.checkpoint.memory import InMemorySaver # Usamos InMemorySaver para simplificar
from langchain_core.messages import SystemMessage       # :contentReference[oaicite:1]{index=1}


def react_agent():
    model = os.getenv("OLLAMA_MODEL", "qwen3:4b")
    llm = ChatOllama(
        model=model,
        temperature=0,
    )
    python_repl = PythonAstREPLTool(
        # locals={"df": df},
        name="python_repl",
        description="Ejecuta código Python sobre el DataFrame df y devuelve el resultado del último statement."
    )
    checkpointer = InMemorySaver()
    system_prompt = SystemMessage("Siempre que puedas, debes usar python_repl para escribirte código en python. Dispones de un dataframe llamado df que contiene los datos de maestro_componentes.csv. Puedes usarlo para responder a las preguntas del usuario.")

    agent_executor = create_react_agent(
        llm,
        [python_repl],
        prompt=system_prompt,
        # checkpointer=checkpointer,
        # callbacks=[StdOutCallbackHandler()]   # imprime en consola cada call
    )
    return agent_executor

graph2 = react_agent()
