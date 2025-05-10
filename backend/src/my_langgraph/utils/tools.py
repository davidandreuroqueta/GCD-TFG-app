from langchain_core.tools import tool

@tool
def multiply(first_number: int, second_number: int) -> int:
    """Multiplica dos números."""
    return first_number * second_number
