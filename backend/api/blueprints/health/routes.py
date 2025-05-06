from . import bp
from flask import jsonify

@bp.route("/health", methods=["GET"])
def health():
    """
    GET /health
    Comprueba que la API está viva.
    """
    return jsonify(status="ok"), 200
