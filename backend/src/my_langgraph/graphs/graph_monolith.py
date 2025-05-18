
import os, uuid
from typing import Dict, Any, List

from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent       #  ReAct helper  :contentReference[oaicite:2]{index=2}
from langgraph.checkpoint.memory import MemorySaver      #  Thread‑level memory  :contentReference[oaicite:3]{index=3}
from langchain_core.messages import SystemMessage       # :contentReference[oaicite:1]{index=1}

from my_langgraph.utils.tools import python_repl
from my_langgraph.utils.utils import get_promt


OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")

def create_graph_monolith(
    model_name: str,
    model_prompt: str,
) -> Any:
    if not model_name:
        raise ValueError("Model name must be provided.")
    if not model_prompt:
        raise ValueError("Model prompt must be provided.")

    model_prompt = get_promt(model_prompt)
    
    llm = ChatOllama(
        base_url=OLLAMA_URL,
        model=model_name,
        temperature=0,
    )
    # Create the agent
    agent = create_react_agent(
        llm,
        tools=[python_repl],
        name="graph_monolith",
        prompt=SystemMessage(model_prompt),
    )
    
    return agent