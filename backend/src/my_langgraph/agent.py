from langgraph.prebuilt import create_react_agent
from langchain_ollama import ChatOllama
import os
from langchain_experimental.tools.python.tool import PythonAstREPLTool
from langgraph.checkpoint.memory import InMemorySaver # Usamos InMemorySaver para simplificar
from langchain_core.messages import SystemMessage       # :contentReference[oaicite:1]{index=1}


def react_agent():
    model = os.getenv("OLLAMA_MODEL", "qwen3:4b")
    url = os.getenv("OLLAMA_URL", "http://localhost:11434")
    llm = ChatOllama(
        base_url=url,
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

graph = react_agent()

from my_langgraph.graph import graph2
