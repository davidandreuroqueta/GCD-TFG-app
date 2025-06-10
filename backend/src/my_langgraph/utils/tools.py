import pandas as pd
from langchain_experimental.tools import PythonAstREPLTool
from typing import Dict, Any
import os

# --- 1) Carga el DataFrame global ---------------------------------
def get_csv_path():
    """
    Obtiene la ruta del archivo CSV maestro con manejo inteligente de rutas.
    
    Returns:
        str: Ruta absoluta al archivo CSV
    
    Raises:
        FileNotFoundError: Si el archivo no existe en ninguna de las rutas probadas
    """
    # Obtener la ruta desde variable de entorno
    csv_path = os.getenv("MAESTRO_CSV_PATH")
    # Obtener directorio raíz del proyecto (4 niveles arriba desde este archivo)
    current_dir = os.path.dirname(__file__)
    project_root = os.path.abspath(os.path.join(current_dir, "..", "..", "..", ".."))
    
    
    if csv_path:
        # Si la ruta es absoluta, usarla tal como está
        if os.path.isabs(csv_path):
            resolved_path = csv_path
        else:
            # Si es relativa, resolverla desde la raíz del proyecto
            resolved_path = os.path.join(project_root, csv_path)
        
        if os.path.exists(resolved_path):
            return resolved_path
    
    # Ruta por defecto: backend/data/maestro_componentes.csv
    default_path = os.path.join(project_root, "backend", "data", "maestro_componentes.csv")
    
    if os.path.exists(default_path):
        return default_path
    
    # Si ninguna ruta funciona, lanzar error
    raise FileNotFoundError(
        f"No se pudo encontrar el archivo CSV en ninguna de las siguientes rutas:\n"
        f"- Variable de entorno MAESTRO_CSV_PATH: {csv_path if csv_path else 'No definida'}\n"
        f"- Ruta por defecto: {default_path}\n"
        f"Por favor, verifica que el archivo exista o configura la variable de entorno MAESTRO_CSV_PATH."
    )

# Obtener la ruta del archivo CSV
csv_path = get_csv_path()
print(f"Cargando CSV desde: {csv_path}")

df = pd.read_csv(csv_path)

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
