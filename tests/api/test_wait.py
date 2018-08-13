import pytest

from bromine.exceptions import TimeoutException
from bromine.utils.wait import Wait

from .. import Mock


def test_wait_until():
    condition = Mock(side_effect=[False, True])
    Wait(1, poll_frequency=0.01).until(condition)
    assert condition.call_count == 2


def test_wait_until_timeout():
    condition = Mock(return_value=False)
    with pytest.raises(TimeoutException):
        Wait(0.1, poll_frequency=0.01).until(condition)
    assert condition.call_count >= 2


def test_wait_until_not():
    condition = Mock(side_effect=[True, False])
    Wait(1, poll_frequency=0.01).until_not(condition)
    assert condition.call_count == 2


def test_wait_until_not_timeout():
    condition = Mock(return_value=True)
    with pytest.raises(TimeoutException):
        Wait(0.1, poll_frequency=0.01).until_not(condition)
    assert condition.call_count >= 2
