from hamcrest import assert_that

from bromine.utils.geometry import Rectangle, RectSize, PIL_box
from bromine.utils.image import Image, ScreenshotFromImage

from .layout import PagePortion


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


class PagePortionScreenshot(PageScreenshot):

    def __init__(self, page, portion):
        super(PagePortionScreenshot, self).__init__(page)
        self._portion = portion

    def _take(self):
        window_image = self._window.get_screenshot().as_image()
        portion = self._get_window_portion()
        portion_image = window_image.crop(PIL_box(portion.rectangle_in_pixels()))
        return ScreenshotFromImage(portion_image)

    def _get_window_portion(self):
        return WindowPortion(self._window, self._portion)


class VisiblePagePortionScreenshot(PagePortionScreenshot):

    def __init__(self, page):
        visible_portion = self._get_visible_portion(page)
        super(VisiblePagePortionScreenshot, self).__init__(page, visible_portion)

    @staticmethod
    def _get_visible_portion(page):
        visible_size = page.visible_size
        return PagePortion(page, (None, None), visible_size, (0, 0))


class SimpleVerticalFullPageScreenshot(PageScreenshot):

    def __init__(self, page):
        super(SimpleVerticalFullPageScreenshot, self).__init__(page)
        self._pixels_per_point = self._page.window.virtual_pixel_ratio

    def _take(self):
        result = self._initialize_result_image()
        for tile in self._page.layout.tiles():
            tile_image = self._get_tile_screenshot(tile)
            offset = self._pixels_per_point * tile.page_offset
            result.paste(tile_image, tuple(offset))
        return ScreenshotFromImage(result)

    def _initialize_result_image(self):
        total_size_in_pixels = self._pixels_per_point * self._page.size
        return Image.new('RGBA', total_size_in_pixels)

    def _get_tile_screenshot(self, tile):
        tile.scroll_into_view()
        return PagePortionScreenshot(self._page, tile).take().as_image()


class WindowPortion(object):

    def __init__(self, window, page_portion):
        self._window = window
        self._page_portion = page_portion

    def rectangle_in_pixels(self):
        upper_left_corner_in_pixels = self._upper_left_corner_in_pixels()
        size_in_pixels = self._size_in_pixels()
        return Rectangle.from_corner_and_size(upper_left_corner_in_pixels, size_in_pixels)

    def _upper_left_corner_in_pixels(self):
        return self._in_pixels(self._upper_left_corner())

    def _upper_left_corner(self):
        address_bar_height = self._window.address_bar_height
        window_margin = RectSize(0, address_bar_height)
        page_margin = self._page_portion.margin
        return window_margin + page_margin

    def _in_pixels(self, value_in_points):
        return self._pixels_per_point() * value_in_points

    def _pixels_per_point(self):
        return self._window.virtual_pixel_ratio

    def _size_in_pixels(self):
        return self._in_pixels(self._size())

    def _size(self):
        return self._page_portion.size
