import six


class CurrentUrlTest(object):

    def __init__(self, current_url, expected_url):
        self.current_url = current_url
        self.expected_url = expected_url

    def __bool__(self):
        return self.current_url == self.expected_url

    if six.PY2:
        __nonzero__ = __bool__
