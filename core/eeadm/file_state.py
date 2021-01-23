"""eeadm file state <file>."""
import logging
import re
import subprocess

from . import EEADM

logging.getLogger(__name__).addHandler(logging.NullHandler)


class LtfseeFile:
    """Object to represent an file on LTFSEE.

    P  2  JD0099JD@POOL_JD@ts4500  MB0355JE@POOL_JE@ts4500  -   -- /gpfs/gpfs0/sample_file
    M  1  MB0355JE@POOL_JE@ts4500  -                        -   -- /gpfs/gpfs0/sample_file2

    State - File State R : Resident, P : Premigrated, M : Migrated
    Replicas - Number replicas
    Tapes - Array of <barcode>@<pool>@<library>
    Path - Path to file
    """

    def __init__(self, state=False, replicas=False, tapes=[], path=False):
        """Create File State Object."""
        # State and Path are required
        if not state:
            raise ValueError("File State is Required")
        if not path:
            raise ValueError("File Path is Required")

        self.state = state
        self.replicas = replicas
        self.tapes = tapes
        self.path = path

    def __str__(self):

        return f"{self.state}  {self.replicas}  {'  '.join(self.tapes)}  -- {self.path}"


class EEADM_File_State(EEADM):
    """
    Wrapper around eeadm file state -s  <path>.

    path - Absolute path to files on filesystem

    Wild cards are accepted (TODO)

    returns list of LtfseeFile objects
    """

    def __init__(self, path):
        """Pass file path to get the state. Globs are acceptable.

        path - IN  file path or shell glob to pass to eeadm file state <path>
        """

        args = ["eeadm", "file", "state", "-s", path]
        logging.debug(f"Calling {args}")
        proc = subprocess.run(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=10,
            check=True,
            universal_newlines=True,
        )

        results = list()
        logging.debug(proc.stdout)
        results.append(proc.stdout)
        # for line in proc.stdout:
        #    logging.debug(line)
        #    results.append(line)

        #        results = [
        #            "P  2  JD0099JD@POOL_JD@ts4500  MB0355JE@POOL_JE@ts4500  -   -- /gpfs/gpfs0/sample_file",
        #            "M  1  MB0355JE@POOL_JE@ts4500  -                        -   -- /gpfs/gpfs0/sample_file2",
        #            "R  0  -                        -                        -   -- /gpfs/gpfs0/sample_file3",
        #        ]

        self.files = []  # Will host list of files matched by glob
        for entry in results:
            match = re.match(
                r"([PMR])\s+(\d+)\s+(\S+)\s+(\S+)\s+(\S+)\s+\-\-\s+(\/.+)", entry
            )
            tapes = []
            for tape in [match[3], match[4], match[5]]:
                if not tape == "-":
                    tapes.append(tape)
            logging.debug(f"File Entry: {entry}")
            self.files.append(
                LtfseeFile(
                    state=match[1], replicas=match[2], tapes=tapes, path=match[6]
                )
            )

    def __len__(self):
        """Length is number of files matched."""
        return len(self.files)
