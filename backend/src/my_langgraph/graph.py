from __future__ import annotations
from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent
from langgraph_supervisor import create_supervisor
from my_langgraph.utils.tools import python_repl, query_maestro, compute_cost
import os 
import os
from dataclasses import dataclass, field
from typing import Dict, List, Any

from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langgraph_supervisor import create_supervisor
from langgraph.graph import StateGraph, END


# ------------------------------------------------------------------
# 0) Shared product state ──────────────────────────────────────────
# ------------------------------------------------------------------
@dataclass
class ProductState:
    user_messages: List[str] = field(default_factory=list)
    product_spec: Dict[str, Any] = field(default_factory=dict)
    components: List[Dict[str, Any]] = field(default_factory=list)
    costs: List[Dict[str, float]] = field(default_factory=list)
    current_step: str | None = None


# ------------------------------------------------------------------
# 1) Small‑LLM model stub (change as needed) ───────────────────────
# ------------------------------------------------------------------
model = os.getenv("OLLAMA_MODEL", "qwen3:4b")
url = os.getenv("OLLAMA_URL", "http://localhost:11434")
llm = ChatOllama(
    base_url=url,
    model=model,
    temperature=0,
)

# ------------------------------------------------------------------
# 2) Low‑level worker agents  (React pattern) ──────────────────────
#     Each gets exactly ONE responsibility & tool bundle
# ------------------------------------------------------------------
# 2.1 Ask‑User agent
def ask_user(question: str) -> str:
    """Dummy placeholder → In production this comes from chat front‑end."""
    return input(question + "\n> ")

ask_user_agent = create_react_agent(
    llm,
    tools=[ask_user],
    name="ask_user_agent",
    prompt="You are an interactive questionnaire. Always call ask_user.",
)

# 2.2 Master‑CSV query agent
from my_langgraph.utils.tools import query_maestro  # you already have utils.tools

csv_agent = create_react_agent(
    llm,
    tools=[python_repl, query_maestro],
    name="csv_lookup_agent",
    prompt=(
        "Usa primero `query_maestro` para filtrar el componente adecuado y, "
        "si necesitas cálculos adicionales sobre el DataFrame, emplea `python_repl`."
    ),
)

calc_agent = create_react_agent(
    llm,
    tools=[compute_cost],
    name="cost_calc_agent",
    prompt=(
        "Aplica `compute_cost` para calcular el coste escalado y con complejidad. "
        "Devuelve un JSON con subtotal y detalles."
    ),
)

# 2.4 User validation
def validate_with_user(text: str) -> str:
    """
    Presenta el presupuesto del componente al usuario y solicita su aprobación o modificación.
    """
    return ask_user(f"Valida o corrige este presupuesto:\n{text}")

validation_agent = create_react_agent(
    llm,
    tools=[validate_with_user],
    name="user_validation_agent",
    prompt="Show the component cost and ask user to approve or modify.",
)

# 2.5 Summarizer
def summarize(data: Dict[str, Any]) -> str:
    """
    Suma los subtotales de cada componente y devuelve el coste total en euros.
    """
    total = sum(c["subtotal"] for c in data["costs"])
    return f"Coste total: {total:.2f} €"

summary_agent = create_react_agent(
    llm,
    tools=[summarize],
    name="summary_agent",
    prompt="Summarize all component costs in Euros with clear table.",
)

# ------------------------------------------------------------------
# 3) Team supervisors  ──────────────────────────────────────────────
#     Each supervisor delegates to ONE OR MORE worker agents above
# ------------------------------------------------------------------
req_team = create_supervisor(
    [ask_user_agent],
    model=llm,
    supervisor_name="requirements_supervisor",
    prompt=(
        "Recopila toda la información necesaria del usuario. "
        "Cuando no falten datos, devuelve un JSON con la especificación completa."
    ),
    output_mode="last_message",
).compile(name="requirements_supervisor")

est_team = create_supervisor(
    [csv_agent, calc_agent],
    model=llm,
    supervisor_name="estimation_supervisor",
    prompt=(
        "Para cada componente pendiente usa csv_lookup_agent y luego cost_calc_agent. "
        "Devuelve un dict con código, descripción, unidad, cantidad, subtotal."
    ),
    output_mode="last_message",
).compile(name="estimation_supervisor")

val_team = create_supervisor(
    [validation_agent],
    model=llm,
    supervisor_name="validation_supervisor",
    prompt="Presenta cada componente al usuario y espera confirmación.",
    output_mode="last_message",
).compile(name="validation_supervisor")

sum_team = create_supervisor(
    [summary_agent],
    model=llm,
    supervisor_name="summary_supervisor",
    prompt="Agrupa lo aprobado y genera un resumen final.",
    output_mode="last_message",
).compile(name="summary_supervisor")

# ------------------------------------------------------------------
# 4) Top‑level supervisor (boss)  ──────────────────────────────────
# ------------------------------------------------------------------
workflow = create_supervisor(
    [req_team, est_team, val_team, sum_team],
    model=llm,
    supervisor_name="master_supervisor",
    prompt=(
        "Eres el supervisor maestro del presupuesto Grantlamp. "
        "Secuencia: 1) requirements_supervisor 2) estimation_supervisor "
        "3) validation_supervisor 4) summary_supervisor. "
        "Avanza sólo cuando cada fase indique 'DONE'."
    ),
    output_mode="full_history",   # continuous stream for UI
)

graph2 = workflow.compile()

# # ------------------------------------------------------------------
# # 5) Entry point for src/my_langgraph/agent.py ───────────────────────────
# # ------------------------------------------------------------------
# def run_budget_assistant(user_first_message: str):
#     initial = ProductState(user_messages=[user_first_message])
#     config = {"configurable": {"thread_id": "grantlamp-session"}}
#     for delta in graph.stream(initial, config):
#         yield delta