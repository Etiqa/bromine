import pytest

from bromine.utils.wait import Wait

from .. import Mock


@pytest.mark.parametrize('bool_seq,iterations', (
    ([False, True, False, True], 2),
    ([False, False, True], 3),
    ([True, True], 1)
))
def test_wait_until_returns_as_soon_as_condition_is_true(bool_seq, iterations):
    condition = Mock(side_effect=bool_seq)
    Wait(10, poll_frequency=0.01).until(condition)
    assert condition.call_count == iterations
