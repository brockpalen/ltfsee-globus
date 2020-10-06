"""Unit tests for advanced_client."""
import logging
from pathlib import Path
from unittest.mock import MagicMock, mock_open, patch

import pytest

from client.advanced_client import nfs_remap, remap_root


@pytest.fixture
def mounts():
    """Fixture data from /proc/mounts."""
    data = "/etc/auto.nfs.dataden /nfs/dataden autofs rw,relatime,fd=29,pgrp=7693,timeout=300,minproto=5,maxproto=5,indirect,pipe_ino=45611 0 0\nradonc-ljungman-dataden.dataden.arc-ts.umich.edu:/gpfs/locker0/ces/dataden/g/radonc-ljungman-dataden /nfs/dataden/radonc-ljungman-dataden nfs rw,nosuid,relatime,vers=3,rsize=1048576,wsize=1048576,namlen=255,hard,noacl,proto=tcp,timeo=600,retrans=5,sec=sys,mountaddr=10.242.97.21,mountvers=3,mountport=32767,mountproto=tcp,local_lock=none,addr=10.242.97.21 0 0"
    return data


def test_nfs_remap(monkeypatch):
    """Remap NFS mount paths to their path on LTFSEE."""
    path = "/nfs/dataden/umms-bleu/myfile.txt"
    logging.debug(f"Path remapping is: {path}")
    monkeypatch.setenv("DEPTH", "4")

    # replace remap_root
    m = MagicMock()
    m.return_value = "/gpfs/locker0/ces/dataden/g/umms-bleu"
    with patch("client.advanced_client.remap_root", m):
        remap_path = nfs_remap(path)

    assert remap_path == "/gpfs/locker0/ces/dataden/g/umms-bleu/myfile.txt"  # nosec


def test_remap_root(mounts):
    """Check correctly matching a path to entries in /proc/mounts."""
    m = mock_open(read_data=mounts)
    with patch("client.advanced_client.open", m):
        mount = remap_root(Path("/nfs/dataden/radonc-ljungman-dataden"))

    assert mount == "/gpfs/locker0/ces/dataden/g/radonc-ljungman-dataden"  # nosec
