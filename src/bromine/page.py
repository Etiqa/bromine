import six


class WebPage(object):

    def __init__(self, url, browser):
        self._url = url
        self._browser = browser

    @property
    def browser(self):
        """Instance of Selenium WebDriver."""
        return self._browser

    @property
    def url(self):
        """Web page's URL."""
        return self._url

    def go_to(self):
        self.browser.get(self.url)

    def is_current_page(self):
        return _CurrentUrlTest(self.browser.current_url, self.url)

    @property
    def title(self):
        return self.browser.title


class _CurrentUrlTest(object):

    def __init__(self, current_url, expected_url):
        self.current_url = current_url
        self.expected_url = expected_url

    def __bool__(self):
        return self.current_url == self.expected_url

    if six.PY2:
        __nonzero__ = __bool__
