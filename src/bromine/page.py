"""
Web page model.
"""

from six.moves.urllib.parse import urljoin

from .utils.url import url_with_given_scheme


class WebPage(object):
    """Represents a Web Page.

    Web pages are grouped into a web application.
    """

    def __init__(self, application, relative_url, name=None, scheme=None):
        if not name:
            name = relative_url
        self._relative_url = relative_url
        self._scheme = scheme
        self._name = name
        self._application = application
        self._add_elements()

    def _add_elements(self):
        """Override this method to declare this page's elements."""

    @property
    def application(self):
        return self._application

    @property
    def browser(self):
        """Instance of Selenium WebDriver."""
        return self.application.browser if self.application else None

    @property
    def name(self):
        """Optional name to identify this web page."""
        return self._name

    @property
    def relative_url(self):
        return self._relative_url

    def url(self, scheme=None):
        """Web page's URL."""
        base_url = self.application.base_url(self._scheme) if self.application else ''
        joined_url = urljoin(base_url, self.relative_url)
        return url_with_given_scheme(joined_url, scheme)

    def go_to(self):
        self.browser.get(self.url())
        assert self.is_current_page()

    def is_current_page(self):
        return self.browser.current_url == self.url()

    @property
    def title(self):
        return self.browser.title
