import six
if six.PY3:
    from collections import UserDict
else:
    from UserDict import IterableUserDict as UserDict # pylint: disable=import-error


class Environment(UserDict):

    def __init__(self, base_url, **kwargs):
        # In py2 IterableUserDict is a classobj, not a new-style class,
        # so super() is not supported :-(
        UserDict.__init__(self, base_url=base_url, **kwargs)

    @property
    def base_url(self):
        return self['base_url']
