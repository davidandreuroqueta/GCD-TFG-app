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
def calcular_coste_unitario(coste: float,
                             lote_maximo_escalado: int,
                             coste_lote_maximo_escalado: float,
                             n: int,
                             multiplicador_simple: float,
                             multiplicador_complejidad: float,
                             dificultad: str = None) -> float:
    """
    Calcula el coste unitario final aplicando el escalado y el multiplicador de complejidad.
    Parámetros:
      coste: coste unitario base.
      lote_maximo_escalado: umbral para coste mínimo.
      coste_lote_maximo_escalado: coste unitario a partir de lote máximo.
      n: número de unidades.
      multiplicador_simple: factor para piezas simples.
      multiplicador_complejidad: factor para piezas complejas.
      dificultad: 'simple' o 'compleja'.
    Retorna:
      Coste unitario ajustado.
    """
    def calcular_coste_unitario_escalado(coste: float, lote_maximo_escalado: int, coste_lote_maximo_escalado: float, n: int) -> float:
        """
        Calcula el coste unitario escalado según el número de unidades (n), usando la lógica de precios escalados:
        - Si n == 1: coste base.
        - Si 1 < n < lote_maximo_escalado: coste + (n-1)*((coste_lote_maximo_escalado - coste)/(lote_maximo_escalado-1)).
        - Si n >= lote_maximo_escalado: coste_lote_maximo_escalado.
        """
        if n == 1:
            return coste
        if 1 < n < lote_maximo_escalado:
            return coste + (n - 1) * ((coste_lote_maximo_escalado - coste) / (lote_maximo_escalado - 1))
        return coste_lote_maximo_escalado
    # Escalado por cantidad
    coste_unitario = calcular_coste_unitario_escalado(coste, lote_maximo_escalado, coste_lote_maximo_escalado, n)
    # Ajuste por complejidad
    if not dificultad:
        return coste_unitario
    if dificultad == 'simple':
        return coste_unitario * multiplicador_simple
    if dificultad == 'compleja':
        return coste_unitario * multiplicador_complejidad
    return coste_unitario
