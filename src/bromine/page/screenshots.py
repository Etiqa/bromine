from hamcrest import assert_that

from bromine.utils.image import Image

from .layout import Tile


class PageScreenshot(object):

    def __init__(self, page):
        self._page = page
        self._window = page.window

    def take(self):
        self._assert_current_page()
        return self._take()

    def _assert_current_page(self):
        assert_that(
            self._page.is_current_page(),
            "{page} is not displayed on browser's current window".format(page=self._page))

    def _take(self):
        raise NotImplementedError


class WindowScreenshot(PageScreenshot):

    def _take(self):
        return self._window.get_screenshot()


class VisiblePortionScreenshot(PageScreenshot):

    def _take(self):
        visible_size = self._page.visible_size
        tile = Tile(self._page, 0, (None, None), visible_size)
        return tile.get_screenshot()


class SimpleVerticalFullPageScreenshot(PageScreenshot):

    def _take(self):
        pixels_per_point = self._page.window.virtual_pixel_ratio
        total_size = self._page.size
        result = Image.new('RGBA', (pixels_per_point*total_size.width, pixels_per_point*total_size.height))
        for tile in self._page.layout.tiles():
            tile.scroll_into_view()
            im = tile.get_screenshot().as_image()
            offset = tile.upper_left_corner
            result.paste(im, (pixels_per_point*offset.x, pixels_per_point*offset.y))
        return result
