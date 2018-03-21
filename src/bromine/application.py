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
        self.pages = self._page_list()

    def _page_list(self): # pylint: disable=no-self-use
        return []

    @property
    def base_url(self):
        return self._base_url

    @property
    def browser(self):
        """Return the WebDriver instance"""
        return self._browser

    @property
    def pages(self):
        return self._pages.values()

    @pages.setter
    def pages(self, pages):
        _pages_dict = {}
        for page in pages:
            assert page.name is not None, 'Registered pages must have a name'
            assert page.name not in _pages_dict, 'Duplicate name "{}"'.format(page.name)
            page.browser = self.browser
            page.url = urljoin(self.base_url, page.url)
            _pages_dict[page.name] = page
        self._pages = _pages_dict # pylint: disable=attribute-defined-outside-init

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
