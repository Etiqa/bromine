from hamcrest import assert_that

# from bromine.utils.geometry import Rectangle, RectSize, PIL_box
# from bromine.utils.image import Image, ScreenshotFromImage


class ElementScreenshot(object):

    def __init__(self, element):
        self._element = element

    def take(self):
        self._assert_element_is_displayed()
        return self._take()

    def _assert_element_is_displayed(self):
        assert_that(
            self._element.is_displayed(),
            "{element} is not displayed on browser's current window".format(element=self._element))

    def _take(self):
        return self._element.get_screenshot()

class ScrollableElementScreenshot(ElementScreenshot):
    pass
