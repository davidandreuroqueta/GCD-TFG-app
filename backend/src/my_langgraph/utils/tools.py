import pandas as pd
from langchain_experimental.tools import PythonAstREPLTool
from typing import Dict, Any
import os

# --- 1) Carga el DataFrame global ---------------------------------
MAESTRO_CSV_PATH = os.getenv("MAESTRO_CSV_PATH", None)
print(os.getcwd())
if MAESTRO_CSV_PATH is None:
    raise ValueError("MAESTRO_CSV_PATH no está definido. Por favor, establece la variable de entorno.")
if not os.path.exists(MAESTRO_CSV_PATH):
    raise FileNotFoundError(f"El archivo {MAESTRO_CSV_PATH} no existe. Por favor, verifica la ruta.")
df = pd.read_csv(MAESTRO_CSV_PATH)

# --- 2) Tool: REPL para inspeccionar el DataFrame -----------------
python_repl = PythonAstREPLTool(
    locals={"df": df},
    name="python_repl",
    description=(
        "Ejecuta código Python sobre el DataFrame global `df` "
        "y devuelve el resultado del último statement."
    ),
)

# --- 3) Tool: filtrar el maestro con reglas estrictas -------------
def query_maestro(query: Dict[str, Any]) -> str:
    """
    Filtra `df` usando las claves entregadas en `query`.
    Ejemplo de `query`: {'tipo': 'Metal Planchas', 'subgrupo': 'Acero', 'regex': 'pintura.*epoxi'}
    """

    mask = pd.Series([True] * len(df))
    if "tipo" in query:
        mask &= df["tipo"].str.fullmatch(query["tipo"], case=False, na=False)
    if "subgrupo" in query:
        mask &= df["subgrupo"].str.contains(query["subgrupo"], case=False, na=False)
    if "regex" in query:
        mask &= df["descripcion"].str.contains(query["regex"], case=False, regex=True, na=False)
    resultado = df[mask]
    if resultado.empty:
        return "[]"
    # devolvemos en JSON compacto
    return resultado.to_json(orient="records")

# --- 4) Tool: cálculo de costes -----------------------------------
def compute_cost(row: Dict[str, Any], n: int, medida: float, complejidad: str | None = None) -> float:
    """
    Aplica la lógica de precios escalados y complejidad.
    `row` es un dict con las columnas del maestro (coste, coste_lote_maximo_escalado, lote_maximo_escalado, unidad_medida, multiplicador_complejidad_*).
    """

    coste = row["coste"]
    coste_lote_max = row["coste_lote_maximo_escalado"]
    lote_max = row["lote_maximo_escalado"]

    if n == 1:
        coste_unit = coste
    elif 1 < n < lote_max:
        coste_unit = coste + (n - 1) * ((coste_lote_max - coste) / (lote_max - 1))
    else:
        coste_unit = coste_lote_max

    subtotal = coste_unit * medida * n

    if complejidad and complejidad.lower() in ("simple", "compleja"):
        mult = row[f"multiplicador_complejidad_{complejidad.lower()}"]
        subtotal *= mult

    return round(subtotal, 2)
