# GCD-TFG App: Automatización de presupuestos personalizados mediante Large Language Models

## 📖 Descripción

Este repositorio presenta el trabajo realizado en mi **Trabajo Final de Grado en Ciencia de Datos** en la **Universidad Politécnica de Valencia**, titulado **"Automatización de presupuestos personalizados mediante Large Language Models"**.

El proyecto implementa múltiples agentes de IA especializados en la elaboración automática de presupuestos para productos industriales, específicamente para la empresa **Grantlamp**. La solución combina:

- **LangGraph**: para definir flujos de trabajo (DAGs) que cargan datos estructurados, razonan sobre costes y estiman precios
- **OpenRouter API**: para acceso a modelos LLM de gran escala (Claude, Gemini, Mistral)
- **Ollama**: para ejecución local de modelos open-source (Llama, Qwen)
- **LangGraph Platform**: servidor local para despliegue y gestión de agentes
- **Análisis comparativo**: evaluación sistemática del rendimiento de diferentes arquitecturas de agentes

## 🤖 Agentes Implementados

El proyecto incluye **6 agentes especializados** con diferentes arquitecturas y modelos:

### Agentes Monolíticos (Single-Agent)
- **`graph_monolith_claude`**: Agente único con Claude 3.5 Sonnet (OpenRouter)
- **`graph_monolith_gemini`**: Agente único con Gemini 2.0 Flash (OpenRouter) 
- **`graph_monolith_mistral`**: Agente único con Mistral Large 2411 (OpenRouter)
- **`graph_monolith_llama`**: Agente único con Llama 3.1 (Ollama local)
- **`graph_monolith_qwen`**: Agente único con Qwen 2.5 (Ollama local)

### Agente Multi-Agente (Dual Architecture)
- **`graph_dual_mix`**: Arquitectura dual con Manager (Llama 3.1) + Coder (Qwen 2.5) ejecutándose en Ollama

> **Arquitecturas**: Los agentes *monolíticos* utilizan una sola herramienta de procesamiento de texto, mientras que el agente *dual* implementa una arquitectura multi-agente donde el Manager coordina las tareas y el Coder ejecuta las estimaciones técnicas.

## 🚀 Características principales

- **Múltiples proveedores LLM**: Soporte para OpenRouter (modelos grandes) y Ollama (modelos locales)
- **Acceso al Maestro de Componentes**: Búsqueda inteligente de piezas similares y precios históricos
- **Estimación automática**: Generación de presupuestos completos con razonamiento paso a paso
- **Análisis de rendimiento**: Evaluación comparativa con métricas de eficiencia y calidad
- **Arquitecturas diversas**: Comparación entre enfoques monolíticos y multi-agente

## 📊 Evaluación y Análisis

El proyecto incluye un **análisis exhaustivo del rendimiento** de los agentes, evaluando:

### Métricas de Calidad (Evaluación Humana)
- **Acceso (0-2)**: Capacidad para acceder y utilizar correctamente el Maestro de Componentes
- **Adecuación (0-10)**: Precisión técnica y coherencia de la respuesta generada

### Métricas de Eficiencia (Objetivas)
- **Tokens consumidos**: Uso de recursos computacionales
- **Tiempo de inferencia**: Velocidad de respuesta
- **Coste económico**: Análisis coste-beneficio por presupuesto

> **Resultados clave**: Los modelos locales de Ollama no lograron completar la tarea de presupuestación completa, mientras que los modelos grandes (Claude, Gemini, Mistral) a través de OpenRouter mostraron diferentes perfiles de rendimiento según la métrica evaluada.

## 🛠️ Prerrequisitos

- **Python 3.11+**
- **Docker** (>=24) y **docker-compose**
- **Node.js 20** y **npm** (opcional, para desarrollo frontend)
- **Git**
- **API Keys**: OpenRouter API key para modelos externos

## 📁 Estructura del proyecto

```text
GCD-TFG-app/
├── backend/
│   └── src/
│       └── my_langgraph/
│           ├── agent.py          # Definición de todos los agentes
│           ├── tools/             # Herramientas de acceso al Maestro de Componentes
│           └── prompts/           # Templates de prompts especializados
├── evaluation/
│   ├── analisis.ipynb            # Análisis comparativo de resultados
│   └── data/                     # Datos de evaluación y métricas
├── frontend/ui-budget/           # Interfaz de usuario (Assistant-UI)
├── models/ollama/                # Modelos locales (bind-mount)
├── ops/
│   └── docker-compose.dev.yml    # Configuración de desarrollo
├── langgraph.json               # Configuración LangGraph Platform
└── README.md
```

## ⚙️ Configuración del entorno

### 1. Configuración inicial
```bash
git clone <repo_url>.git
cd GCD-TFG-app
mkdir -p models/ollama
```

### 2. Variables de entorno
Crea un archivo `.env` con:
```bash
OPENROUTER_API_KEY=tu_openrouter_api_key
LANGCHAIN_API_KEY=tu_langchain_api_key  # Opcional, para tracing
```

### 3. Levantar servicios con Docker
```bash
docker-compose -f ops/docker-compose.dev.yml up --build
```

### 4. Servidor LangGraph local
Para ejecutar los agentes localmente usando LangGraph Platform:
```bash
# Instalar dependencias
pip install -e ./backend

# Ejecutar servidor local
langgraph dev
```

Ver [documentación oficial](https://langchain-ai.github.io/langgraph/tutorials/langgraph-platform/local-server/) para más detalles.

## 📥 Gestión de modelos

### Modelos Ollama (Locales)
```bash
# Acceder al contenedor
docker-compose exec llm bash

# Descargar modelos necesarios
ollama pull llama3.1:8b
ollama pull qwen2.5:7b
```

### Modelos OpenRouter (Externos)
Los siguientes modelos se acceden vía API:
- Claude 3.5 Sonnet
- Gemini 2.0 Flash  
- Mistral Large 2411

## 🔬 Ejecutar evaluaciones

Para reproducir el análisis comparativo:

```bash
# Ejecutar notebook de análisis
jupyter notebook evaluation/analisis.ipynb

# O usando el entorno Docker
docker-compose exec backend jupyter notebook --allow-root
```

## 💡 Caso de uso: Grantlamp

El sistema está optimizado para generar presupuestos de productos industriales para **Grantlamp**, integrando:

- **14-18 componentes** por presupuesto típico
- **Acceso al Maestro de Componentes** (base de datos propietaria)
- **Estimación de precios** basada en similitudes y precios históricos
- **Razonamiento técnico** paso a paso documentado

### Ejemplo de flujo:
1. El usuario solicita un presupuesto con especificaciones técnicas
2. El agente accede al Maestro de Componentes para buscar piezas similares
3. Se calculan estimaciones basadas en precios históricos y ajustes técnicos
4. Se genera un presupuesto detallado con justificación de cada componente

## 📈 Resultados del TFG

## 📈 Resultados del TFG

### Principales hallazgos:

#### 🎯 **Conclusión estratégica clave**
Tras evaluar múltiples enfoques tecnológicos, **el GPT privado de OpenAI se consolida como la solución óptima**, ofreciendo el mejor balance calidad-coste-previsibilidad para la automatización de presupuestos.

#### 🔍 **Evaluación comparativa de modelos**
- **GPT y Claude 3.5 Sonnet**: Líderes indiscutibles en calidad técnica y coherencia
- **Gemini 2.0 Flash**: Más económico y rápido, pero con menor finura en el razonamiento  
- **Mistral Large 2411**: Rendimiento intermedio con buena velocidad de respuesta
- **Modelos locales (8B parámetros)**: **Descartados** por incapacidad para seguir consistentemente la metodología de negocio

#### ⚖️ **Trade-offs tecnológicos identificados**
- **LLMaaS vs. Autoalojado**: Las soluciones como servicio minimizan drásticamente la carga de DevOps
- **Calidad vs. Coste**: Claude ofrece máxima calidad pero con alto coste y latencia; Gemini es económico pero menos preciso
- **Soberanía vs. Practicidad**: El autoalojamiento garantiza control total de datos pero introduce complejidad operativa prohibitiva

#### 📊 **Impacto operativo medido**
- **Reducción del tiempo de presupuestación: >50%**
- **Precisión mantenida: ±10%** respecto a estimación experta
- **Metodología "piezas de lego"**: Validada y aceptada por usuarios finales en entorno de producción

#### 🏗️ **Complejidad de desarrollo**
- **GPT privado**: Mantenimiento marginal centrado en mejora de prompts
- **LangGraph + Assistant-UI**: Requiere CI/CD completo, monitorización y soporte especializado continuo
- **Modelos pequeños autoalojados**: Inviables por inconsistencia en seguimiento de lógica de negocio

### Publicaciones y documentación:
- Memoria completa del TFG (disponible tras defensa)
- Análisis estadístico en `evaluation/analisis.ipynb`
- Métricas detalladas por agente y sesión de prueba

## 🤝 Contribuciones

Este es un proyecto académico, pero las contribuciones son bienvenidas para:
- Mejoras en las arquitecturas de agentes
- Nuevos modelos o proveedores LLM
- Optimizaciones en las métricas de evaluación
- Extensiones para otros dominios industriales

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Véase `LICENSE` para más detalles.

---

**Trabajo Final de Grado** | **Universidad Politécnica de Valencia** | **Grado en Ciencia de Datos**