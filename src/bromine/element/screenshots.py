from hamcrest import assert_that
from bromine.utils.geometry import Rectangle, RectSize, PIL_box
from bromine.utils.image import Image, ScreenshotFromImage


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
    

class ElementPortionScreenshot(ElementScreenshot):
    
    def __init__(self, element, portion):
        super(ElementPortionScreenshot, self).__init__(element)
        self._portion = portion

    def _take(self):
        element_image = self._element.get_screenshot().as_image()
        portion = self._get_element_portion()
        portion_image = element_image.crop(PIL_box(portion.rectangle_in_pixels()))
        return ScreenshotFromImage(portion_image)
    
    def _get_element_portion(self):
        return ElementPortion(self._element.browser.window, self._portion)

class ScrollableElementScreenshot(ElementScreenshot):
    def __init__(self, element):
        super(ScrollableElementScreenshot, self).__init__(element)
        self._pixels_per_point = self._element.browser.window.virtual_pixel_ratio

    def _take(self):
        result = self._initialize_result_image()
        for tile in self._element.layout.tiles():
            tile_image = self._get_tile_screenshot(tile)
            offset = self._pixels_per_point * tile.element_offset
            result.paste(tile_image, tuple(offset))
        return ScreenshotFromImage(result)

    def _initialize_result_image(self):
        total_size_in_pixels = self._pixels_per_point * self._element.scroll_size
        return Image.new('RGBA', total_size_in_pixels)

    def _get_tile_screenshot(self, tile):
        tile.scroll_into_view()
        return ElementPortionScreenshot(self._element, tile).take().as_image()

class ElementPortion(object):
    
    def __init__(self, window, element_portion):
        self._window = window
        self._element_portion = element_portion

    def rectangle_in_pixels(self):
        upper_left_corner_in_pixels = self._upper_left_corner_in_pixels()
        size_in_pixels = self._size_in_pixels()
        return Rectangle.from_corner_and_size(upper_left_corner_in_pixels, size_in_pixels)

    def _upper_left_corner_in_pixels(self):
        return self._in_pixels(self._upper_left_corner())

    def _upper_left_corner(self):
        element_margin = self._element_portion.margin
        return element_margin

    def _in_pixels(self, value_in_points):
        return self._pixels_per_point() * value_in_points

    def _pixels_per_point(self):
        return self._window.virtual_pixel_ratio

    def _size_in_pixels(self):
        return self._in_pixels(self._size())

    def _size(self):
        return self._element_portion.size