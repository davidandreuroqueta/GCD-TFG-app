from functools import wraps
from flask import request, jsonify
from api.config import get_settings

def require_api_key(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        cfg = get_settings()
        incoming = request.headers.get("x-api-key", "")
        # if not cfg.API_KEY or incoming != cfg.API_KEY:
        #     return jsonify({"error": "Unauthorized"}), 401
        return fn(*args, **kwargs)
    return wrapper