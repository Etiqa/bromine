# pylint: disable=missing-docstring

import bromine


def test_version():
    assert hasattr(bromine, '__version__')
