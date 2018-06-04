import re

import requests

from six.moves.urllib.parse import urlsplit, urlunsplit, urljoin


def url_with_given_scheme(url, scheme=None):
    if scheme is None:
        return url
    else:
        parts = list(urlsplit(url))
        parts[0] = scheme
        return urlunsplit(parts)


class RobotsTxt(object):

    def __init__(self, base_url, verify_ssl=True):
        self._url = urljoin(base_url, 'robots.txt')
        self._verify_ssl = verify_ssl
        self._response = None

    @property
    def url(self):
        return self._url

    def _get(self):
        if self._response is None:
            self._response = requests.get(self.url, verify=self._verify_ssl)
        return self._response

    @property
    def status_code(self):
        r = self._get()
        return r.status_code

    @property
    def directives(self):
        r = self._get()
        directives = []
        for line in r.text.splitlines():
            line = line.strip()
            if line.startswith('#'):
                continue
            line = re.sub(r'[\s]+\#.*', '', line)
            if line:
                split = line.split(':', 1)
                if len(split) != 2:
                    continue
                field, value = [x.strip() for x in split]
                directive = (field, value)
            directives.append(directive)
        return directives
