from functools import wraps

from flask import current_app, request
from flask_restx import abort


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        token = None

        if "X-API-KEY" in request.headers:
            token = request.headers["X-API-KEY"]

        if not token:
            abort(401, message="Missing or invalid auth tokens")

        if token != current_app.config["AUTH_KEY"]:
            abort(401, message="Missing or invalid auth tokens")

        return f(*args, **kwargs)

    return decorated
