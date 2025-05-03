# backend/Dockerfile
FROM python:3.10-slim-bullseye

WORKDIR /app

ENV PIP_ROOT_USER_ACTION=ignore

# Instala Poetry y dependencias
COPY pyproject.toml poetry.lock /app/
RUN pip install --no-cache-dir poetry \
 && poetry config virtualenvs.create false \
 && poetry install --only main,dev

# Copia el resto del código
COPY . /app

# Expone el puerto
EXPOSE 8000

# Comando por defecto
CMD ["flask", "--app", "api.app", "--debug", "run", "--host", "0.0.0.0", "--port", "8000"]