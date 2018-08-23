from bromine.utils.geometry import RectSize


class PageScroller(object):

    def __init__(self, page):
        self._page = page
        self._browser = page._browser

    @property
    @RectSize.wrapped
    def level(self):
        return self._javascript('''
            return [window.pageXOffset, window.pageYOffset];
        ''')

    def by(self, width=None, height=None):
        scroll_options = {}
        if width is not None:
            scroll_options['left'] = width
        if height is not None:
            scroll_options['top'] = height
        self._javascript('window.scrollBy(arguments[0])', scroll_options)

    def to(self, x=None, y=None):
        scroll_options = {}
        if x is not None:
            scroll_options['left'] = x
        if y is not None:
            scroll_options['top'] = y
        self._javascript('window.scrollTo(arguments[0])', scroll_options)

    def to_upper_left_corner(self):
        self.to(0, 0)

    def _javascript(self, script, *script_arguments):
        return self._browser.execute_script(script, *script_arguments)
