"""Cases for eeadm/file_state.py."""
from unittest.mock import MagicMock, patch

import pytest  # noqa

import core
from core.eeadm.recall import EEADM_Recall


@patch("sh.eeadm", create=True)
def test_EEADM_Recall(monkeypatch):
    """Call EEADM_Recall it should return right away and find command in background."""

    mock_sh = MagicMock(name="sh-echo")
    mock_sh.return_value = "/gpfs/gpfs0/file.dat"
    monkeypatch.setattr(core.eeadm.recall.sh, "echo", mock_sh)
    # monkeypatch.setattr(core.eeadm.recall.sh, "eeadm", mock_sh)
    recall = EEADM_Recall("/gpfs/gpfs0/*", library="tplib_l")
    print(mock_sh.call_args_list)
