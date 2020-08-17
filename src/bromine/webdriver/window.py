from hamcrest import assert_that, equal_to

from ..utils.geometry import RectSize
from ..utils.image import ScreenshotFromPngBytes


class Window(object):

    def __init__(self, browser):
        self._browser = browser

    @property
    @RectSize.wrapped
    def outer_size(self):
        size = self._browser.get_window_size()
        return (size['width'], size['height'])

    @property
    @RectSize.wrapped
    def inner_size(self):
        return self._browser.execute_script(
            'return [window.innerWidth, window.innerHeight];')

    @property
    def virtual_pixel_ratio(self):
        return self._browser.execute_script('return window.devicePixelRatio;')

    @property
    def physical_pixel_ratio(self):
        return self.virtual_pixel_ratio

    @property
    def address_bar_height(self):
        if hasattr(self._browser, 'address_bar_height'):
            return self._browser.address_bar_height
        else:
            return 0

    @property
    def bar_shadow_height(self):
        if hasattr(self._browser, 'bar_shadow_height'):
            return self._browser.bar_shadow_height
        else:
            return 0

    def get_screenshot(self):
        png_bytes = self._browser.get_screenshot_as_png()
        return ScreenshotFromPngBytes(png_bytes)


class ResizableWindow(Window):

    @Window.outer_size.setter
    def outer_size(self, value):
        self._browser.set_window_size(*value)
        assert_that(self.outer_size, equal_to(value), 'Outer Window Size')

    @Window.inner_size.setter
    def inner_size(self, value):
        size_adjustment = value - self.inner_size
        try:
            self.outer_size += size_adjustment
        except AssertionError:
            pass
        assert_that(self.inner_size, equal_to(value), 'Inner Window Size')

    def maximize(self):
        self._browser.maximize_window()
