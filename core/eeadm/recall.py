"""eeadm recall."""
import logging

import sh

from . import EEADM

logging.getLogger(__name__).addHandler(logging.NullHandler)


class EEADM_Recall(EEADM):
    """
    Wrapper around eeadm recall.

    path - Absolute path to files on filesystem
    library - If multi-Library system required

    Wild cards are accepted (TODO)

    returns sucess if submitted
    """

    def __init__(self, path, library=None):
        """Pass file path to get the state. Globs are acceptable.
        path - IN  file path or shell glob to pass to eeadm file state <path>
        library - IN If multi-Library system required
        """

        args = ["recall"]
        if library:
            args += ["-l", library]

        logging.debug(f"For file {path} using library {library}")
        sh.sleep("30", _bg=True)

        # sh.eeadm(args, _bg=True)
