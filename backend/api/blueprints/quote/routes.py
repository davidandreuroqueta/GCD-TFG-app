from flask import Blueprint, request, jsonify
from api.graphs.agent import process_input
from api.utils.auth import require_api_key
from api.config import get_settings


bp = Blueprint("quote", __name__)

@bp.route("/v1/quote", methods=["POST"])
@require_api_key
def quote():
    """
    POST /v1/quote
    - x-api-key validado
    - Header opcional x-conversation-id
    - Procesa con process_input(conversation_id, prompt)
    """
    cfg = get_settings()
    conv_id = request.headers.get("x-conversation-id", None)
    if not conv_id:
        # si no se provee, usamos un default por sesión (puede ser IP+timestamp)
        conv_id = "default"

    body = request.get_json() or {}
    prompt = body.get("prompt", "")

    response = process_input(conv_id, prompt)
    return jsonify({"response": response}), 200
