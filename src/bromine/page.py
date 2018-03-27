"""
Web page model.
"""

class WebPage(object):
    """Represents a Web Page.

    Web pages can be grouped into a web application.
    """

    def __init__(self, url, browser=None, name=None):
        self._url = url
        self._browser = browser
        self._name = name
        self._add_elements()

    @property
    def url(self):
        """Web page's URL."""
        return self._url

    @url.setter
    def url(self, value):
        self._url = value

    @property
    def browser(self):
        """Instance of Selenium WebDriver."""
        return self._browser

    @browser.setter
    def browser(self, value):
        self._browser = value

    @property
    def name(self):
        """Optional name to identify this web page."""
        return self._name

    def _add_elements(self):
        """Override this method to declare this page's elements."""
        pass
