import six
if six.PY3:
    from unittest.mock import Mock, PropertyMock
else:
    from mock import Mock, PropertyMock # pylint: disable=import-error

__all__ = (Mock.__name__, PropertyMock.__name__)
