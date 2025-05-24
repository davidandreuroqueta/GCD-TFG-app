from __future__ import annotations
import os
from dataclasses import dataclass, field
from typing_extensions import TypedDict, Annotated, Literal
from typing import List, Dict, Any

from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from my_langgraph.utils.tools import python_repl  # nuestro REPL + DataFrame
from my_langgraph.utils.utils import get_promt

# ---------------------------------------------------------------------------
# 1. Estado compartido
# ---------------------------------------------------------------------------
class DualState(TypedDict, total=False):
    messages: Annotated[list, add_messages]  # historial completo manager+coder
    task: str | None                         # orden en lenguaje natural
    result: str | None                       # respuesta codificada del coder

# ---------------------------------------------------------------------------
# 2. Modelo LLM
# ---------------------------------------------------------------------------
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
MODEL_MANAGER = os.getenv("OLLAMA_MANAGER", "llama3:8b-instruct")
MODEL_CODER   = os.getenv("OLLAMA_CODER", "qwen3:8b-instruct")


def create_graph_dual(manager_llm_name, coder_llm_name, manager_prompt, coder_prompt) -> Any:
    if not manager_llm_name or not coder_llm_name:
        raise ValueError("Model names must be provided.")

    manager_prompt = get_promt(manager_prompt)
    coder_prompt = get_promt(coder_prompt)

    manager_llm = ChatOllama(
        base_url=OLLAMA_URL,
        model=manager_llm_name,
        temperature=0,
    )
    coder_llm   = ChatOllama(
        base_url=OLLAMA_URL,
        model=coder_llm_name,
        temperature=0,
    )

    # ---------------------------------------------------------------------------
    # 3. Nodo Manager (Conversacional / Project-Manager)
    # ---------------------------------------------------------------------------

    manager_agent = create_react_agent(
        manager_llm,
        tools=[python_repl],  # se registra para que pueda emitir tool_call
        prompt=manager_prompt,
        name="manager_agent",
    )

    def manager_node(state: DualState) -> DualState:
        """Ejecuta el agente conversacional y extrae la tool_call (si existe)."""
        output = manager_agent.invoke({"messages": state["messages"]})
        state["messages"] += output["messages"]

        # Si hubo llamada a herramienta, guardar la task
        last_ai = output["messages"][-1]
        tcalls = getattr(last_ai, "tool_calls", None)
        if tcalls:
            state["task"] = tcalls[0]["args"]["query"]
        else:
            state["task"] = None
        return state

    # ---------------------------------------------------------------------------
    # 4. Nodo Coder (Python REPL executor)
    # ---------------------------------------------------------------------------

    coder_agent = create_react_agent(
        coder_llm,
        tools=[python_repl],
        prompt=coder_prompt,
        name="coder_agent",
    )

    def coder_node(state: DualState) -> DualState:
        """Ejecuta python_repl con la tarea y guarda el resultado."""
        query = state["task"]
        if query:
            tool_call = f"python_repl({query})"
            output = coder_agent.invoke(
                {
                    "messages": state["messages"]
                    + [
                        {
                            "type": "tool",
                            "name": "python_repl",
                            "args": {"query": query},
                        }
                    ]
                }
            )
            state["messages"] += output["messages"]
            state["result"] = output["messages"][-1].content
            # Limpiar para el siguiente ciclo
            state["task"] = None
        return state

    # ---------------------------------------------------------------------------
    # 5. Grafo con edge condicional
    # ---------------------------------------------------------------------------
    g = StateGraph(DualState)
    g.add_node("manager", manager_node)
    g.add_node("coder", coder_node)
    g.set_entry_point("manager")

    def needs_coder(state: DualState) -> bool:
        return state["task"] is not None

    g.add_conditional_edges(
        "manager",
        needs_coder,
        {True: "coder", False: END},
    )
    g.add_edge("coder", "manager")

    # workflow = g.compile()
    return g.compile()


# ---------------------------------------------------------------------------
# 6. Export graph2 para LangGraph Cloud
# ---------------------------------------------------------------------------
# graph2 = workflow.compile()  # <= requerido por tu servidor LangGraph
