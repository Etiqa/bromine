"""
Web page model.
"""

from six.moves.urllib.parse import urljoin

from .utils import url_with_given_scheme


class WebPage(object):
    """Represents a Web Page.

    Web pages are grouped into a web application.
    """

    def __init__(self, url, name=None):
        self._url = url
        self._name = name
        self.application = None
        self._add_elements()

    @property
    def application(self):
        return self._application

    @application.setter
    def application(self, value):
        self._application = value

    def url(self, scheme=None):
        """Web page's URL."""
        base_url = self.application.base_url() if self.application else ''
        joined_url = urljoin(base_url, self._url)
        return url_with_given_scheme(joined_url, scheme)

    @property
    def browser(self):
        """Instance of Selenium WebDriver."""
        return self.application.browser if self.application else None

    @property
    def name(self):
        """Optional name to identify this web page."""
        return self._name

    def _add_elements(self):
        """Override this method to declare this page's elements."""
        pass
