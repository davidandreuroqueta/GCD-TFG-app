from flask import Flask
from api.config import Settings
from api.extensions import init_extensions

# Importar blueprints
from api.blueprints.health.routes import bp as health_bp
from api.blueprints.quote.routes import bp as quote_bp
from api.blueprints.stream.routes import bp as stream_bp

def create_app() -> Flask:
    app = Flask(__name__)
    # Carga .env y config pydantic
    app.config.from_object(Settings())

    # Monta CORS, JWT, metrics…
    init_extensions(app)

    # Registro de blueprints
    app.register_blueprint(health_bp)                 # → GET /health
    app.register_blueprint(quote_bp, url_prefix="")   # → POST /v1/quote
    app.register_blueprint(stream_bp, url_prefix="")  # → GET  /v1/stream

    return app


# Si quieres ejecutar directamente:
if __name__ == "__main__":
    create_app().run(host="0.0.0.0", port=8000, debug=True)