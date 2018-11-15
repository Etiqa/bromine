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
        scroll_options = {'top': 0, 'left': 0}
        if width is not None:
            scroll_options['left'] = width
        if height is not None:
            scroll_options['top'] = height
        self._javascript('window.scrollBy({},{})'.format(scroll_options['left'],scroll_options['top']))

    def to(self, x=None, y=None):
        level = self.level
        scroll_options = {'top': level.height, 'left': level.width}
        if x is not None:
            scroll_options['left'] = x
        if y is not None:
            scroll_options['top'] = y
        self._javascript('window.scrollTo({},{})'.format(scroll_options['left'],scroll_options['top']))

    def to_upper_left_corner(self):
        self.to(0, 0)

    def _javascript(self, script, *script_arguments):
        return self._browser.execute_script(script, *script_arguments)
