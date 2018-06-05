import six
if six.PY3:
    from unittest.mock import Mock, PropertyMock, patch
else:
    from mock import Mock, PropertyMock, patch # pylint: disable=import-error


assert (Mock, PropertyMock, patch)
