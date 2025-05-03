# GCD-TFG App: Agente de Presupuestos con LangGraph + Flask + Assistant-UI

## 📖 Descripción
Este repositorio contiene un prototipo de un agente de IA para la elaboración de presupuestos de productos, basado en:

- **LangGraph (Python)**: para definir flujos de trabajo (DAGs) que cargan datos estructurados, razonan sobre costes y estiman precios de piezas similares.
- **Flask**: expone el agente mediante una API REST con rutas de presupuestado y streaming (SSE).
- **Assistant-UI (React + Next.js)**: interfaz de chat moderna que consume la API y muestra el razonamiento paso a paso.
- **Ollama / TGI / vLLM**: servidor de modelos LLM de código abierto (localmente) para generar estimaciones.
- **Docker & Docker Compose**: entorno reproducible para levantar el backend, frontend y LLM en contenedores.

## 🚀 Características principales

- Carga de ficheros CSV con costes de componentes.
- Búsqueda de piezas similares usando heurísticas o embeddings.
- Estimación de precios mediante prompt a LLM.
- Streaming de pasos de razonamiento a la UI.
- Volúmenes para persistir pesos de modelos dentro del proyecto.

## 🛠️ Prerrequisitos

- **Docker** (>=24) y **docker-compose**
- **Python 3.11**
- **Node.js 20** y **npm**
- **Git**

## 📁 Estructura del proyecto

```text
GCD-TFG-app/
├── backend/                # API Flask + LangGraph
│   ├── api/app.py          # Entrypoint de Flask
│   ├── graph/              # Definición de nodos y flujos LangGraph
│   ├── models/             # Pydantic schemas
│   └── pyproject.toml      # Configuración Poetry
├── frontend/ui-budget/     # Assistant-UI template (Next.js)
├── models/ollama/          # Carpeta bind-mount para pesos de LLM
├── ops/                    # Operaciones y scripts de infraestructura
│   └── docker-compose.dev.yml
├── LICENSE
└── README.md
```

## ⚙️ Entorno de desarrollo

1. Clona el repositorio y crea la carpeta de modelos:
   ```bash
   git clone <repo_url>.git
   cd GCD-TFG-app
   mkdir -p models/ollama
   ```

2. Levanta los contenedores:
   ```bash
   docker-compose -f ops/docker-compose.dev.yml up --build
   ```

3. Comprueba los servicios:
   - **LLM**: disponible en `http://localhost:11434` (podrás hacer `ollama pull llama2` dentro del contenedor).
   - **API**: health-check en `http://localhost:8000/health`.
   - **UI**: abre `http://localhost:3000` en tu navegador.

## 📥 Gestión de modelos LLM

Dentro del contenedor `llm` (Ollama):
```bash
# Accede al contenedor
docker-compose exec llm bash
# Descarga un modelo, p.ej:
ollama pull llama2
```
Los pesos se guardarán en `models/ollama/` en tu máquina.

## 💡 Uso básico

1. Desde la UI, envía un BOM (lista de componentes y cantidades) en el chat.
2. El backend procesará el CSV, ejecutará el grafo LangGraph y mostrará cada paso.
3. Obtendrás un desglose de costes y una estimación final.

## 📈 Roadmap de desarrollo

Para más detalles, consulta los _Issues_ y _Projects_ de este repositorio. Principales hitos:

- Fase 1: Entorno dev + Hello World LangGraph.
- Fase 2: Nodos de carga CSV y estimación.
- Fase 3: Streaming SSE y UI React.
- Fase 4: Observabilidad (Prometheus/Grafana).
- Fase 5: Despliegue en staging/producción.

## 📝 Contribuciones

¡Bienvenidas! Por favor abre Pull Requests y discute las mejoras en los _Issues_.

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Véase `LICENSE` para más detalles.