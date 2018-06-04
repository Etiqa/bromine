import six
if six.PY3:
    from unittest.mock import Mock, PropertyMock, patch
else:
    from mock import Mock, PropertyMock, patch # pylint: disable=import-error

__all__ = (Mock.__name__, PropertyMock.__name__, patch.__name__)
