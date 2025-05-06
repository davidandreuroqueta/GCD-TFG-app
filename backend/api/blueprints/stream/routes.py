from . import bp
from flask import Response, stream_with_context
from api.utils.auth import require_api_key


@bp.route("/v1/stream", methods=["GET"])
@require_api_key
def stream():
    """
    GET /v1/stream
    Ejemplo básico de SSE: emite tres eventos dummy.
    """
    def event_stream():
        yield "data: iniciando stream…\n\n"
        yield "data: paso intermedio\n\n"
        yield "data: stream finalizado\n\n"

    return Response(
        stream_with_context(event_stream()),
        mimetype="text/event-stream",
    )
