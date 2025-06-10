#!/bin/bash
# filepath: c:\Users\dandr\coding\GCD-TFG-app\pull_models.sh

# Comprobar que se han proporcionado los argumentos necesarios
if [ "$#" -lt 2 ]; then
    echo "Uso: $0 <dirección_api> <modelo1> [<modelo2> ...]"
    echo "Ejemplo: $0 https://353f-34-44-156-99.ngrok-free.app qwen3:8b mistral:7b phi3:mini"
    exit 1
fi

# Guardar la dirección API
API_URL="$1"
shift  # Eliminar el primer argumento (la dirección)

# Comprobar que la URL es válida
if [[ ! "$API_URL" =~ ^https?:// ]]; then
    echo "Error: La dirección API debe comenzar con http:// o https://"
    exit 1
fi

echo "Descargando modelos desde: $API_URL"

# Procesar cada modelo
for model in "$@"; do
    echo "Descargando modelo: $model..."
    
    # Realizar la llamada API con curl
    response=$(curl -s -X POST "$API_URL/api/pull" -d "{\"model\": \"$model\"}")
    
    # Comprobar si la respuesta contiene un error
    if [[ "$response" == *"error"* ]]; then
        echo "Error al descargar $model: $response"
    else
        echo "Modelo $model: Solicitud enviada correctamente"
        echo "Respuesta: $response"
    fi
    
    echo "------------------------"
done

echo "Proceso completado."