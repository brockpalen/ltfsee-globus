#!/usr/bin/env python
"""Simple client using the ltfsee_globus API to submit recall reqeusts."""

import logging
import sys
from pathlib import Path

import requests
from environs import Env

env = Env()


def remap_root(root):
    """Read /proc/mounts and remap path to server path.

    Eg. /nfs/dataden/export --> /gpfs/locker0/ces/g/dataden/export
    """
    with open("/proc/mounts", "r") as mounts:
        split_mounts = [s.split() for s in mounts.read().splitlines()]

    # compare root to mount
    for p in split_mounts:
        if p[1] == str(root):  # root is pathlib.Path() compare string
            new_root = p[0].split(":")[1]
            logging.debug(f"Matched {root} to {p[1]} New Root: {new_root}")
            return new_root

    # shuld not get here raise
    logging.critical(f"Did not find mount for {root}")
    raise ValueError


def nfs_remap(path):
    """Remap filesystems that are exported over NFS to their path on GPFS.

    Eg:
    radonc-ljungman-dataden.dataden.arc-ts.umich.edu:/gpfs/locker0/ces/dataden/g/radonc-ljungman-dataden /nfs/dataden/radonc-ljungman-dataden
    umms-bleu.dataden.arc-ts.umich.edu:/gpfs/locker0/ces/dataden/g/umms-bleu                             /nfs/dataden/umms-bleu

    Eg:
    /nfs/dataden/umms-bleu/myfile.txt --> /gpfs/locker0/ces/dataden/g/umms-bleu/myfile.txt
    """

    # get old_root based on depth, eg '3' /nfs/dataden/umms-bleu/  '2' /nfs/dataden  etc.
    p = Path(path)

    depth = env.int("DEPTH", 4)
    parts = p.parts

    old_root = Path(*parts[:depth])
    logging.debug(f"Subdir root is: {old_root}")

    # get 'stub'  eg '3'  /myfile.txt  '2' umms-bleu/myfile.txt
    stub = Path(*parts[depth:])
    logging.debug(f"Stub is: {stub}")

    # find match, in mount list, parse server path eg /gpfs/locker0/ces/dataden/g/umms-bleu
    new_root = remap_root(old_root)

    # prepend server path to stub and return
    remap_path = Path(new_root).joinpath(stub)
    logging.debug(f"Remapped path is: {remap_path}")
    return str(remap_path)  # return path as a string


if __name__ == "__main__":
    if env("DEBUG", False):
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.WARNING)

    # required
    # Path to file
    path = env("GLOBUS_STAGE_PATH")
    logging.debug(f"Checking status of: {path}")

    # remap path for NFS mounts
    path = nfs_remap(path)

    # Globus taskid
    taskid = env("GLOBUS_STAGE_TASKID")
    logging.debug(f"Globus TaskId: {taskid}")

    # Timeout value in seconds
    timeout = env("TIMEOUT", 10)

    # TODO: Hostname for API server
    apiserver = env("LTFSEE_URL", "http://localhost:5000")

    data = {"path": path, "globus_taskid": taskid}

    r = requests.post(
        f"{apiserver}/api/v0.5/globus_recall/globus_recall", json=data, timeout=timeout
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
