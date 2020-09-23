"""Main API importation into Flask."""
from flask import Blueprint
from flask_restx import Api

# from apis.file_state import api as file_state


# https://github.com/OAI/OpenAPI-Specification/blob/master/versions/2.0.md
# http://flask-restplus.readthedocs.io/en/stable/swagger.html
authorizations = {"basic": {"type": "basic"}}

blueprint = Blueprint("api", __name__, url_prefix="/api/v0.5")
api = Api(
    blueprint,
    title="ARC LTFSEE API",
    version="0.5",
    description="Provide API access to LTFSEE commands not currently supported by the vendor API",
    authorizations=authorizations,
    # All API metadatas
)

# api.add_namespace(file_state)
