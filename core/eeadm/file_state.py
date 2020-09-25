"""eeadm file state <file>."""
import logging

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
