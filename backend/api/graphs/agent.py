# backend/api/graphs/agent.py

import pandas as pd
from pathlib import Path
from langgraph.checkpoint.memory import InMemorySaver # Usamos InMemorySaver para simplificar
from langgraph.prebuilt import create_react_agent
from langchain_experimental.tools.python.tool import PythonAstREPLTool
# from langchain_core.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_core.callbacks.stdout import StdOutCallbackHandler
from langchain_core.messages import SystemMessage       # :contentReference[oaicite:1]{index=1}

from api.clients.model_client import get_model_client

ROOT = Path(__file__).parents[2]
df = pd.read_csv(ROOT / "data" / "maestro_componentes.csv")
print(df.head())

python_repl = PythonAstREPLTool(
    locals={"df": df},
    name="python_repl",
    description="Ejecuta código Python sobre el DataFrame df y devuelve el resultado del último statement."
)

llm = get_model_client()
checkpointer = InMemorySaver()
system_prompt = SystemMessage("Siempre que puedas, debes usar python_repl para escribirte código en python. Dispones de un dataframe llamado df que contiene los datos de maestro_componentes.csv. Puedes usarlo para responder a las preguntas del usuario.")
agent_executor = create_react_agent(
    llm,
    [python_repl],
    prompt=system_prompt,
    checkpointer=checkpointer,
    # callbacks=[StdOutCallbackHandler()]   # imprime en consola cada call
)


def process_input(conversation_id: str, user_input: str) -> str:
    """
    Ejecuta el agente React-style con memoria gestionada por LangGraph.
    - Invoca al agent pasando el input del usuario y el conversation_id como thread_id.
    - El checkpointer se encarga de recuperar y guardar el historial.
    - Obtiene la última respuesta del asistente y la devuelve.
    """
    agent_input = {"messages": [("human", user_input)]}

    result = agent_executor.invoke(
        agent_input,
        config={"configurable": {"thread_id": conversation_id}} # Pasamos el thread_id en el config
    )

    messages = result["messages"]
    last_msg = messages[-1]

    assistant_text = None
    if isinstance(last_msg, tuple):
         assistant_text = last_msg[13]
    elif hasattr(last_msg, 'content'):
        assistant_text = last_msg.content

    return assistant_text