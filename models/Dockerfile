FROM ollama/ollama:latest

# Instalar curl
RUN apt-get update && apt-get install -y curl

# Copiar el script entrypoint al contenedor
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Establecer el entrypoint
ENTRYPOINT ["/entrypoint.sh"]