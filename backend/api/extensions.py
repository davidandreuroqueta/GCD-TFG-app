from flask_cors import CORS
from flask_jwt_extended import JWTManager
from prometheus_flask_exporter import PrometheusMetrics


def init_extensions(app):
    """
    Inicializa extensiones de Flask según configuración.
    - CORS: permite peticiones cross-origin.
    - JWTManager: registrado sólo si JWT_SECRET_KEY está definido.
    - PrometheusMetrics: registrado si PROMETHEUS_ENABLE=True.
    """
    # CORS para todos los orígenes
    CORS(app)

    # JWT (si el usuario ha puesto una clave secreta)
    if app.config.get("JWT_SECRET_KEY"):
        JWTManager(app)

    # Métricas Prometheus
    if app.config.get("PROMETHEUS_ENABLE"):
        PrometheusMetrics(app)
