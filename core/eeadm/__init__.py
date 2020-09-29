"""Module for manipulating eeadm commands for specturm archive."""

import logging

logging.getLogger(__name__).addHandler(logging.NullHandler)


class EEADM:
    """Base class for other classes."""

    def __init__(self):
        """Empty constuctor."""
        pass
