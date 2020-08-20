from ..utils.geometry import RectSize

class ElementScroller(object):

    _SCROLL_BY_JS = "arguments[0].scrollBy({},{})"
    _LEVEL_JS = "return [arguments[0].scrollLeft, arguments[0].scrollTop];"

    def __init__(self, element):
        self._element = element
        self._browser = element._browser
    
    @property
    @RectSize.wrapped
    def level(self):
        return self._javascript(ElementScroller._LEVEL_JS,self._element.dom_element)

    def by(self, width=None, height=None):
        scroll_options = {'top': 0, 'left': 0}
        if width is not None:
            scroll_options['left'] = width
        if height is not None:
            scroll_options['top'] = height
        self._javascript(ElementScroller._SCROLL_BY_JS.format(scroll_options['left'], scroll_options['top']), self._element.dom_element)

    def to(self, x=None, y=None):
        level = self.level
        scroll_options = {'top': level.height, 'left': level.width}
        if x is not None:
            scroll_options['left'] = x
        if y is not None:
            scroll_options['top'] = y
        self._javascript('arguments[0].scrollTo({},{})'.format(scroll_options['left'], scroll_options['top']), self._element.dom_element)
    
    def to_upper_left_corner(self):
        self.to(0, 0)

    def into_view(self):
        self._javascript('arguments[0]scrollIntoView();', self._element.dom_element)

    def _javascript(self, script, *script_arguments):
        return self._browser.execute_script(script, *script_arguments)
