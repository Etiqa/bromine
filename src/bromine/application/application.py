"""
Web application model.
"""


class Application(object):
    """Represents an Application"""


class WebApplication(Application):
    """Represents a Web Application."""

    def __init__(self, base_url, browser):
        self._base_url = base_url
        self._browser = browser
        self._current_page = None

    @property
    def base_url(self):
        return self._base_url

    @property
    def browser(self):
        """Return the WebDriver instance"""
        return self._browser

    @property
    def current_page(self):
        """Logical current page."""
        # TODO: explain what 'logical' means and why we define a setter
        return self._current_page

    @current_page.setter
    def current_page(self, page):
        self._current_page = page
