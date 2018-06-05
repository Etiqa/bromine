"""
Web application model.
"""

from ..exceptions import NoSuchPageError
from ..utils.url import url_with_given_scheme
from ..utils.robots_txt import RobotsTxt


class Application(object):
    """Represents an Application"""


class WebApplication(Application):
    """Represents a Web Application."""

    def __init__(self, environment, browser):
        self._environment = environment
        self._browser = browser
        self._current_page = None
        self._pages = {}
        self._add_pages()

    def _add_pages(self): # pylint: disable=no-self-use
        pass

    def base_url(self, scheme=None):
        return url_with_given_scheme(self._environment.base_url, scheme)

    @property
    def browser(self):
        """Return the WebDriver instance"""
        return self._browser

    def add_page(self, page):
        if not page.name:
            raise ValueError("Page's name must not be empty")
        if page.name in self._pages:
            raise ValueError('Duplicate name "{}"'.format(page.name))
        if page.application is not self:
            raise ValueError("Page's application is inconsistent")
        self._pages[page.name] = page

    def get_page(self, name):
        """Retrieve a previously registered web page."""
        try:
            return self._pages[name]
        except KeyError:
            raise NoSuchPageError(name)

    @property
    def current_page(self):
        """Logical current page."""
        # TODO: explain what 'logical' means and why we define a setter
        return self._current_page

    @current_page.setter
    def current_page(self, page):
        registered_page = self.get_page(page.name)
        if not isinstance(page, type(registered_page)):
            raise NoSuchPageError(type(page)) # TODO: raise more informative exception class
        self._current_page = page

    def robots_txt(self, scheme=None, **kwargs):
        return RobotsTxt(self.base_url(scheme), **kwargs)
