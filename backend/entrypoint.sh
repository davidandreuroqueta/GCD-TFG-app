#!/usr/bin/env sh
# langgraph/entrypoint.sh

# 1) (Re)instalamos el paquete en editable, sobre el /app montado
pip install -e .

# 2) Arrancamos LangGraph VIA python -m para asegurarnos de que
#    use la instalación local y no un CLI global desfasado
exec python -m langgraph dev
