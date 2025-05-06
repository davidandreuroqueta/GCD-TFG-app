# from typing import TypedDict
# from langgraph.graph import START, END, StateGraph

# from .nodes import simple_llm_node


# class SimpleState(TypedDict):
#     prompt: str
#     response: str

# workflow = StateGraph(SimpleState)
# workflow.add_node("simple", simple_llm_node)
# workflow.add_edge(START, "simple")
# workflow.add_edge("simple", END)
# SIMPLE_GRAPH = workflow.compile()

# def run_simple_graph(prompt: str) -> str:
#     """Función que ejecuta el grafo y devuelve sólo la respuesta."""
#     init_state: SimpleState = {"prompt": prompt, "response": ""}
#     final_state = SIMPLE_GRAPH.invoke(init_state)
#     return final_state["response"]
