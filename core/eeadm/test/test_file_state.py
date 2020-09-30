"""Cases for eeadm/file_state.py."""
import logging
from contextlib import ExitStack as does_not_raise

import pytest

from core.eeadm.file_state import EEADM_File_State, LtfseeFile

# [root@ltfs204 gpfs0]# eeadm file state sample* -s
# P  2  JD0099JD@POOL_JD@ts4500  MB0355JE@POOL_JE@ts4500  -   -- /gpfs/gpfs0/sample_file
# M  1  MB0355JE@POOL_JE@ts4500  -                        -   -- /gpfs/gpfs0/sample_file2


@pytest.mark.parametrize(
    "kwargs,expex",
    [
        (
            {
                "state": "M",
                "replicas": 1,
                "tapes": ["MB0355JE@POOL_JE@ts4500"],
                "path": "/gpfs/gpfs0/sample_file",
            },
            does_not_raise(),
        ),
        (
            {
                "state": "M",
                "replicas": 1,
                "tapes": ["MB0355JE@POOL_JE@ts4500"],
                "path": "",  # path is required
            },
            pytest.raises(ValueError, match=r"File Path is Required"),
        ),
        (
            {
                "state": "",  # State Required
                "replicas": 1,
                "tapes": ["MB0355JE@POOL_JE@ts4500"],
                "path": "/gpfs/gpfs0/sample_file",  # path is required
            },
            pytest.raises(ValueError, match=r"File State is Required"),
        ),
        ({}, pytest.raises(ValueError)),  # empty options fails
    ],
)
def test_LtfseeFile(kwargs, expex):
    """Test creation of LtfseeFile object.

    kwargs : Inputs to LtfseeFile()
    expex  : Expected Exception to check for
    """
    with expex:
        LtfseeFile(**kwargs)


def test_EEADM_File_state():
    """Calls EEADM_File_State on the bogus list of files which returns 3 files."""
    files = EEADM_File_State("/gpfs/gpfs0/*")
    logging.debug(files)
    for entry in files.files:
        logging.debug(entry)
    assert len(files) == 3  # nosec
