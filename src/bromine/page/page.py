from .current_url_test import CurrentUrlTest
from .scroll import PageScroller
from .size import Html5DocumentSize
from .layout import SimpleVerticalLayout


class WebPage(object):

    _size = Html5DocumentSize

    def __init__(self, url, browser):
        self._url = url
        self._browser = browser
        self._size = self.__class__._size(self)

    @property
    def browser(self):
        """Instance of Selenium WebDriver."""
        return self._browser

    @property
    def window(self):
        return self._browser.window

    @property
    def url(self):
        return self._url

    def go_to(self):
        self.browser.get(self.url)

    def is_current_page(self):
        return CurrentUrlTest(self.browser.current_url, self.url)

    @property
    def title(self):
        return self.browser.title

    @property
    def size(self):
        return self._size.total()

    @property
    def visible_size(self):
        return self._size.visible()

    @property
    def scroll(self):
        return PageScroller(self)

    @property
    def layout(self):
        return SimpleVerticalLayout(self)
