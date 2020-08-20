from ..utils.geometry import RectSize

_SCROLL_SIZE = "return [arguments[0].scrollWidth,arguments[0].scrollHeight];"


class Html5ElementSize(object):

    def __init__(self, element):
        self._element = element
        self._browser = element._browser

    @RectSize.wrapped
    def size(self):
        size = self._element.dom_element.size
        return [size["width"], size["height"]]

    @RectSize.wrapped
    def scroll_size(self):
        return self._javascript(_SCROLL_SIZE, self._element.dom_element)

    def _javascript(self, script, *script_arguments):
        return self._browser.execute_script(script, *script_arguments)
