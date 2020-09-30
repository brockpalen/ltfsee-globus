"""Cases for eeadm/file_state.py."""
import pytest  # noqa

from core.eeadm.recall import EEADM_Recall


def test_EEADM_Recall():
    """Call EEADM_Recall it should return right away and find command in background."""
    recall = EEADM_Recall("/gpfs/gpfs0/*", library="tplib_l")
