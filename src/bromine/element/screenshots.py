from hamcrest import assert_that

from bromine.utils.geometry import Rectangle, RectSize, PIL_box
from bromine.utils.image import Image, ScreenshotFromImage


class ElementScreenshot(object):

    def __init__(self, web_element):
        self._web_element = web_element

    def take(self):
        self._assert_element_is_displayed()
        return self._take()

    def _assert_element_is_displayed(self):
        assert_that(
            self._web_element.is_displayed(),
            "{web_element} is not displayed on browser's current window".format(web_element=self._web_element))

    def _take(self):
        return self._web_element.get_screenshot()