class WebPage(object):

    def __init__(self, url, browser=None, name=None):
        self._url = url
        self._browser = browser
        self._name = name
        self._add_elements()

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        self._url = value

    @property
    def browser(self):
        return self._browser

    @browser.setter
    def browser(self, value):
        self._browser = value

    @browser.setter
    def browser(self, value):
        self._browser = value

    @property
    def name(self):
        return self._name

    def _add_elements(self):
        pass
