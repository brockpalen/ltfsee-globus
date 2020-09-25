"""API for eeadm file state."""
import logging

from flask import request, url_for
from flask_restx import Namespace, Resource, fields, marshal

logging.getLogger(__name__).addHandler(logging.NullHandler)

api = Namespace(
    "file_state", description="Get state of a file in archive eeadm file state"
)

# model for returning data from eeadm file state -s
# https://www.ibm.com/support/knowledgecenter/ST9MBR_1.3.0/ee_eeadm_file_state_command_output.html
file_state_model = api.model(
    "file_state", {"state": fields.String, "replicas": fields.Integer,}
)


# model for the input of a file
# must be abolute path
file_parser = api.parser()
file_parser.add_argument("path", type=str, required=True, help="absolute path to file")


# create teh API
@api.route("/file_state")
class FileState(Resource):
    @api.marshal_with(file_state_model)
    @api.expect(file_parser, validate=True)
    def post(self, **kwargs):
        args = file_parser.parse_args()
        path = args["path"]

        logging.debug(f"Checking state of {path} from {request.remote_addr}")
        return {"state": "M", "replicas": 2}
