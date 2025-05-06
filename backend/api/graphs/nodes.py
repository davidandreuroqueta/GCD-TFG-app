# from api.clients.model_client import get_model_client

# def simple_llm_node(state: dict) -> dict:
#     """
#     Nodo LangGraph que lee `state["prompt"]`, llama al LLM
#     y añade `state["response"]`.
#     """
#     client = get_model_client()
#     prompt = state.get("prompt", "")
#     response = client.predict(prompt)
#     state["response"] = response
#     return state
