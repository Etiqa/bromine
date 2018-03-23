"""
Web application model.
"""

from six.moves.urllib.parse import urljoin

from .exceptions import NoSuchPageError


class Application(object):
    """Represents an Application"""


class WebApplication(Application):
    """Represents a Web Application."""

    def __init__(self, base_url, browser):
        self._base_url = base_url
        self._browser = browser
        self._current_page = None
        self._pages = {}
        self._add_pages()

    def _add_pages(self): # pylint: disable=no-self-use
        pass

    @property
    def base_url(self):
        return self._base_url

    @property
    def browser(self):
        """Return the WebDriver instance"""
        return self._browser

    def add_page(self, page):
        if page.name is None:
            raise ValueError('Registered pages must have a name')
        if page.name in self._pages:
            raise ValueError('Duplicate name "{}"'.format(page.name))
        page.browser = self.browser
        page.url = urljoin(self.base_url, page.url)
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
