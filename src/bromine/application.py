"""
Web application model.
"""

from .exceptions import NoSuchPageError


class WebApplication(object):
    """Represents a Web Application."""

    def __init__(self, base_url, browser):
        self.__pages = {}
        self.__current_page = None
        self._base_url = base_url
        self._browser = browser

    def add_page(self, name, page):
        """Register a web page with the application."""
        #page.name = name
        #page.browser= self.browser
        self.__pages[name] = page

    def get_page(self, name):
        """Retrieve a previously registered web page."""
        try:
            return self.__pages[name]
        except KeyError:
            raise NoSuchPageError(name)

    @property
    def current_page(self):
        """Logical current page."""
        # TODO: explain what 'logical' means and why we define a setter
        return self.__current_page

    @current_page.setter
    def current_page(self, page):
        if not page in self.__pages.values():
            raise NoSuchPageError(page)
        self.__current_page = page

    @property
    def base_url(self):
        return self._base_url

    @property
    def browser(self):
        """Return the WebDriver instance"""
        return self._browser
