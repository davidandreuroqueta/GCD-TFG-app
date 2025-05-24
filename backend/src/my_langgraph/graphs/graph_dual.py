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
from langgraph_swarm import create_swarm, create_handoff_tool

from my_langgraph.utils.tools import python_repl, calcular_coste_unitario # nuestro REPL + DataFrame
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

    transfer_to_coder = create_handoff_tool(
        agent_name="coder_agent",
        description="Transfer user to the coding assistant.",
    )
    transfer_to_manager = create_handoff_tool(
        agent_name="manager_agent",
        description="Transfer user to the manager assistant.",
    )   
    
    manager_agent = create_react_agent(
        manager_llm,
        tools=[transfer_to_coder],  # se registra para que pueda emitir tool_call
        prompt=manager_prompt,
        name="manager_agent",
    )

    coder_agent = create_react_agent(
        coder_llm,
        tools=[python_repl, calcular_coste_unitario, transfer_to_manager],
        prompt=coder_prompt,
        name="coder_agent",
    )

    swarm = create_swarm(
        agents=[manager_agent, coder_agent],
        default_active_agent="manager_agent",
    )

    # workflow = g.compile()
    return swarm.compile()


# ---------------------------------------------------------------------------
# 6. Export graph2 para LangGraph Cloud
# ---------------------------------------------------------------------------
# graph2 = workflow.compile()  # <= requerido por tu servidor LangGraph
