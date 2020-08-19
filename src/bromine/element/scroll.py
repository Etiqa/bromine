_SCROLL_BY = "arguments[0].scrollBy({},{})"

class ElementScroller(object):

    def __init__(self, element):
        self._element = element
        self._browser = element._browser

    def by(self, width=None, height=None):
        scroll_options = {'top': 0, 'left': 0}
        if width is not None:
            scroll_options['left'] = width
        if height is not None:
            scroll_options['top'] = height
        self._javascript(_SCROLL_BY.format(scroll_options['left'], scroll_options['top']), self._element.dom_element)

    def to(self, x=None, y=None):
        raise NotImplementedError

    def to_upper_left_corner(self):
        raise NotImplementedError

    def _javascript(self, script, *script_arguments):
        return self._browser.execute_script(script, *script_arguments)
