#!/usr/bin/env python
"""Simple client using the ltfsee_globus API to submit recall reqeusts."""

import logging
import sys
from pathlib import Path

import requests
from environs import Env

env = Env()


def remap_root_mounts(root):
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


def remap_root_autofs(root, autofs):
    """Read /etc/auto.* and remap root to server path.

    eg /nfs/dataden/export --> /gpfs/locker0/ces/g/dataden/export

    root:  Path to root depth eg  /nfs/turbo/export
    """

    with open(autofs, "r") as mounts:
        split_mounts = [s.split() for s in mounts.read().splitlines()]

    # compare root/export to mount
    export = str(root).split("/")[-1]  # split root eg /nfs/dataden/export
    logging.debug(f"Found export name: {export}")
    for p in split_mounts:
        if p[0] == export:
            new_root = p[2].split(":")[1]
            logging.debug(f"Matched {root} to {p[1]} New Root: {new_root}")
            return new_root

    # shuld not get here raise
    logging.critical(f"Did not find mount for {root}")
    raise ValueError


def nfs_remap(path, depth, autofs=None):
    """Remap filesystems that are exported over NFS to their path on GPFS.

    Eg:
    radonc-ljungman-dataden.dataden.arc-ts.umich.edu:/gpfs/locker0/ces/dataden/g/radonc-ljungman-dataden /nfs/dataden/radonc-ljungman-dataden
    umms-bleu.dataden.arc-ts.umich.edu:/gpfs/locker0/ces/dataden/g/umms-bleu                             /nfs/dataden/umms-bleu

    Eg:
    /nfs/dataden/umms-bleu/myfile.txt --> /gpfs/locker0/ces/dataden/g/umms-bleu/myfile.txt
    """

    # get old_root based on depth, eg '3' /nfs/dataden/umms-bleu/  '2' /nfs/dataden  etc.
    p = Path(path)

    parts = p.parts

    old_root = Path(*parts[:depth])
    logging.debug(f"Subdir root is: {old_root}")

    # get 'stub'  eg '3'  /myfile.txt  '2' umms-bleu/myfile.txt
    stub = Path(*parts[depth:])
    logging.debug(f"Stub is: {stub}")

    # find match, in mount list, parse server path eg /gpfs/locker0/ces/dataden/g/umms-bleu
    if autofs:
        new_root = remap_root_autofs(old_root, autofs)
    else:
        new_root = remap_root_mounts(old_root)

    # prepend server path to stub and return
    remap_path = Path(new_root).joinpath(stub)
    logging.info(f"Remapped path is: {remap_path}")
    return str(remap_path)  # return path as a string


if __name__ == "__main__":

    # Configuration
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

    # Timeout value in seconds
    timeout = env("TIMEOUT", 10)
    logging.debug(f"Timeout set to: {timeout}")

    # TODO: Hostname for API server
    apiserver = env("LTFSEE_URL", "http://localhost:5000")
    logging.debug(f"LTFSEE Server is: {apiserver}")

    # autofs config file to read, else use /proc/mounts
    autofs = env("AUTOFS")
    logging.debug(f"Using AutoFS file: {autofs}")

    # how far depth we should look to find the 'export' name in the root
    # eg:  4  /nfs/dataden/<export>,   3 /nfs/export etc
    depth = env.int("DEPTH", 4)
    logging.debug(f"DEPTH is set to {depth}")

    # main
    # remap path for NFS mounts
    path = nfs_remap(path, depth=depth, autofs=autofs)
    logging.info(f"Remapped path: {path}")

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
