#!/usr/bin/env python
"""Simple client using the ltfsee_globus API to submit recall reqeusts."""

import logging
import sys

import requests
from environs import Env

env = Env()
if env("DEBUG", False):
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.WARNING)

# required
# Path to file
path = env("GLOBUS_STAGE_PATH")
logging.info(f"Checking status of: {path}")

# Globus taskid
taskid = env("GLOBUS_STAGE_TASKID")
logging.info(f"Globus TaskId: {taskid}")

# X-API-KEY AUTH_KEY
auth_key = env("AUTH_KEY")
headers = {"X-API-KEY": auth_key}

# TODO: Hostname for API server
apiserver = env("LTFSEE_URL", "http://localhost:5000")

data = {"path": path, "globus_taskid": taskid}

r = requests.post(
    f"{apiserver}/api/v0.5/globus_recall/globus_recall", json=data, headers=headers
)

if r.status_code == 201:
    r_data = r.json()
    print(r_data["state"])
    sys.exit(0)  # Globus requires exit 0
if r.status_code == 404:  # not found
    print("No such file on archive", file=sys.stderr)
    sys.exit(2)
else:  # wrong status code error
    logging.error(f"ERROR response {r.status_code} Payload: {r.text}")
    sys.exit(-1)
