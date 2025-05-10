# langgraph/Dockerfile
FROM python:3.11-slim

# 1) Evitamos pyc y buffering
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

WORKDIR /app

# 2) Copiamos metadatos y código completo para que pip install -e encuentre el paquete
COPY pyproject.toml langgraph.json ./
COPY . .

# 3) Instalamos deps del sistema, nuestro paquete editable y el CLI, suprimiendo el warning
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --upgrade pip --root-user-action=ignore && \
    pip install -e . --root-user-action=ignore && \
    pip install "langgraph-cli[inmem]" --root-user-action=ignore

# 4) Exponemos el puerto de LangGraph
EXPOSE 2024

# 5) Arrancamos con el CLI instalado, no con python -m
ENTRYPOINT ["langgraph", "dev"]
