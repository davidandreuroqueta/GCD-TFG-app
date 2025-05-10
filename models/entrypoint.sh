#!/bin/bash
# entrypoint.sh
ollama serve &

# Esperar que arranque el servidor
sleep 5

# Primer request para cargar qwen3:4b en RAM
curl http://localhost:11434/api/generate -d '{
  "model": "qwen3:4b",
  "prompt": "Warming up model",
  "stream": false
}'

# Mantener en foreground
wait
