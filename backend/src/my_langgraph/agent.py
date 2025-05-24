# from langgraph.prebuilt import create_react_agent
# from langchain_ollama import ChatOllama
# import os
# from langchain_experimental.tools.python.tool import PythonAstREPLTool
# from langgraph.checkpoint.memory import InMemorySaver # Usamos InMemorySaver para simplificar
# from langchain_core.messages import SystemMessage       # :contentReference[oaicite:1]{index=1}


# def react_agent():
#     model = os.getenv("OLLAMA_MODEL", "qwen3:4b")
#     url = os.getenv("OLLAMA_URL", "http://localhost:11434")
#     llm = ChatOllama(
#         base_url=url,
#         model=model,
#         temperature=0,
#     )
#     python_repl = PythonAstREPLTool(
#         # locals={"df": df},
#         name="python_repl",
#         description="Ejecuta código Python sobre el DataFrame df y devuelve el resultado del último statement."
#     )
#     checkpointer = InMemorySaver()
#     system_prompt = SystemMessage("Siempre que puedas, debes usar python_repl para escribirte código en python. Dispones de un dataframe llamado df que contiene los datos de maestro_componentes.csv. Puedes usarlo para responder a las preguntas del usuario.")

#     agent_executor = create_react_agent(
#         llm,
#         [python_repl],
#         prompt=system_prompt,
#         # checkpointer=checkpointer,
#         # callbacks=[StdOutCallbackHandler()]   # imprime en consola cada call
#     )
#     return agent_executor

# graph = react_agent()

# from my_langgraph.graph import graph2

from my_langgraph.graphs.graph_monolith import create_graph_monolith
from my_langgraph.graphs.graph_dual import create_graph_dual

graph_monolith_llama = create_graph_monolith(model_name="llama3.1", model_prompt="graph_monolith_v1")
graph_monolith_qwen = create_graph_monolith(model_name="qwen3:8b", model_prompt="graph_monolith_v1")
graph_dual_mix = create_graph_dual(
    manager_llm_name="llama3.1",
    coder_llm_name="qwen3:8b",
    manager_prompt="graph_dual_manager_v1",
    coder_prompt="graph_dual_coder_v1",
)

graph_monolith_claude = create_graph_monolith(
    model_name="anthropic/claude-3.7-sonnet",
    model_prompt="graph_monolith_LLM",
    ollama=False
)
graph_monolith_gemini = create_graph_monolith(
    model_name="google/gemini-2.5-flash-preview-05-20",
    model_prompt="graph_monolith_gemini",
    ollama=False
)
# graph_monolith_qwen = create_graph_monolith(model_name="qwen3:8b")
