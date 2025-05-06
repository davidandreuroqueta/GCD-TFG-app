from flask import Blueprint

bp = Blueprint("health", __name__)

# Importar rutas para que al importar este paquete se registren
from .routes import *  # noqa: F401,F403
