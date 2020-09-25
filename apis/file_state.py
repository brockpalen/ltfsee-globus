"""API for eeadm file state."""
import logging

from flask import request
from flask_restx import Namespace, Resource, fields

logging.getLogger(__name__).addHandler(logging.NullHandler)

api = Namespace(
    "file_state", description="Get state of a file in archive eeadm file state"
)

# model for returning data from eeadm file state -s
# https://www.ibm.com/support/knowledgecenter/ST9MBR_1.3.0/ee_eeadm_file_state_command_output.html
file_state_model = api.model(
    "file_state", {"state": fields.String, "replicas": fields.Integer}
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

    @api.marshal_with(file_state_model)
    @api.expect(file_model, validate=True)
    @api.response(404, "No such file")
    def post(self, **kwargs):
        """POST method to send payload of file path to check status of."""
        path = request.json["path"]

        logging.debug(f"Checking state of {path} from {request.remote_addr}")
        return {"state": "M", "replicas": 2}
