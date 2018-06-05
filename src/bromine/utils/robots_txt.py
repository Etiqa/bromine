import re
from six.moves.urllib.parse import urljoin

import requests


class RobotsTxt(object):

    def __init__(self, base_url, verify_ssl=True):
        self._url = urljoin(base_url, 'robots.txt')
        self._verify_ssl = verify_ssl
        self._response = None

    @property
    def url(self):
        return self._url

    def _fetch(self):
        if self._response is None:
            self._response = requests.get(self.url, verify=self._verify_ssl)
        return self._response

    @property
    def status_code(self):
        resp = self._fetch()
        return resp.status_code

    @property
    def directives(self):
        resp = self._fetch()
        return self.parse_directives(resp.text)

    @staticmethod
    def parse_directives(text):
        directives = []
        for line in text.splitlines():
            line = line.strip()
            if line.startswith('#'):
                continue
            line = re.sub(r'[\s]+#.*', '', line)
            if line:
                split = line.split(':', 1)
                if len(split) != 2:
                    continue
                field, value = [x.strip() for x in split]
                directive = (field, value)
                directives.append(directive)
            else:
                directives.append('')
        return tuple(directives)
