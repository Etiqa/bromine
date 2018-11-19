"""
see https://javascript.info/size-and-scroll
"""

from textwrap import dedent

from ..utils.geometry import RectSize


class Html5DocumentSize(object):

    def __init__(self, page):
        self._browser = page._browser

    @RectSize.wrapped
    def total(self):
        return self.__javascript('''
            Math.max(
                body[scrollDimension],
                body[offsetDimension],
                documentElement[scrollDimension],
                documentElement[offsetDimension],
                documentElement[clientDimension])
        ''')

    @RectSize.wrapped
    def visible(self):
        return self.__javascript('''
            Math.min(
                documentElement[clientDimension],
                windowInnerDimension)
        ''')

    def __javascript(self, size_definition):
        template_script = '''
            var body = document.body;
            var documentElement = document.documentElement;
            function dimension(name) {
                var clientDimension = "client" + name;
                var scrollDimension = "scroll" + name;
                var offsetDimension = "offset" + name;
                var windowInnerDimension = window["inner" + name];
                return (%s);
            }
            return [dimension("Width"), dimension("Height")];
        '''
        script = template_script % self.__dedent(size_definition)
        return self._browser.execute_script(script)

    def __dedent(self, size_definition):
        return dedent(size_definition).strip()
