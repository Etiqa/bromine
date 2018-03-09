# pylint: disable=missing-docstring

from types import ModuleType
import bromine


def test_import():
    assert isinstance(bromine, ModuleType)


def test_version():
    assert hasattr(bromine, '__version__')
