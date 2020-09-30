"""API for requesting a recall of a file

Checks the state of a file requsted if it's Premigrated or Resident it returns 'resident'
If state is Migrated submitts a migrate requst and caches for some amount of time

Optonally can specify library to recall from TODO
Optionally use globus task ID to select library to recall from TODO
"""

import logging
from http import HTTPStatus

from flask import request
from flask_restx import Namespace, Resource, fields

from core.eeadm.file_state import EEADM_File_State

logging.getLogger(__name__).addHandler(logging.NullHandler)

api = Namespace(
    "globus_recall",
    description="Submit requst for state of file recall if not on disk cache",
)


recall_model = api.model(
    "recall_request",
    {
        "path": fields.String(required=True),
        "globus_taskid": fields.String(required=True),
        "library": fields.String,
    },
)

response_model = api.model(
    "recall", {"state": fields.String(required=True, example="resident")}
)


# create teh API
@api.route("/globus_recall")
class GlobusRecall(Resource):
    """API Provider for globus style staging requests."""

    @api.marshal_with(response_model, code=HTTPStatus.CREATED.value)
    @api.expect(recall_model, validate=True)
    @api.response(HTTPStatus.NOT_FOUND.value, "No Such file")
    @api.response(HTTPStatus.CREATED.value, "Requst for recall / state created")
    def post(self, **kwargs):
        """POST method to send payload of to recall file if not exist."""
        path = request.json["path"]
        taskid = request.json["globus_taskid"]
        library = request.json["library"]

        # TODO select library
        # if library use it
        # else if one library configured use that library
        # else if multiple configured use hash(taskid) % 2 to load balance
        # else assume single library and don't include

        # pass in the path including wild cards to get list of file states
        file_state = EEADM_File_State(path)

        logging.debug(file_state.files[1].state)

        if file_state.files[1].state in ["R", "P"]:  # resident or premigrated
            return {"state": "resident"}, HTTPStatus.CREATED

        # file is migrated state recall
        return {"state": "archived"}, HTTPStatus.CREATED