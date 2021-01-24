"""API for eeadm file state."""
from http import HTTPStatus

from flask import request
from flask_restx import Namespace, Resource, fields

from core.eeadm.file_state import EEADM_File_State
from ltfsee_globus.auth import token_required

api = Namespace(
    "file_state", description="Get state of a file in archive eeadm file state"
)

# model for returning data from eeadm file state -s
# https://www.ibm.com/support/knowledgecenter/ST9MBR_1.3.0/ee_eeadm_file_state_command_output.html
file_state_model = api.model(
    "file_state",
    {
        "state": fields.String,
        "replicas": fields.Integer,
        "tapes": fields.List(fields.String),
        "path": fields.String,
    },
)

# model for the input of a file
# must be abolute path
file_model = api.model("file", {"path": fields.String})


# create the API
@api.route("/file_state")
class FileState(Resource):
    """API Provider class for eeadm file state.

    https://www.ibm.com/support/knowledgecenter/ST9MBR_1.3.0/ee_eeadm_file_state_command_output.html
    """

    @api.marshal_list_with(file_state_model, code=HTTPStatus.CREATED.value)
    @api.expect(file_model, validate=True)
    @api.response(HTTPStatus.NOT_FOUND.value, "No such file")
    @api.response(HTTPStatus.CREATED.value, "Request for file state created")
    @token_required
    def post(self, **kwargs):
        """POST method to send payload of file path to check status of files."""
        path = request.json["path"]

        # pass in the path including wild cards to get list of file states
        file_state = EEADM_File_State(path)

        api.logger.debug(file_state.files)

        api.logger.info(f"Checking state of {path} from {request.remote_addr}")
        return file_state.files, HTTPStatus.CREATED
