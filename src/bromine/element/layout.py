from hamcrest import assert_that, equal_to

from bromine.utils.geometry import Rectangle, RectSize
from bromine.utils.wait import Wait
from selenium.common.exceptions import TimeoutException


class SimpleVerticalLayout(object):

    def __init__(self, element):
        total_width, total_height = element.scroll_size
        visible_width, visible_height = element.size
        #Need to be fixed for Windows the scrollbar width should be removed
        # assert total_width == visible_width
        self._element = element
        self._width = total_width
        self._total_height = total_height
        self._max_tile_height = visible_height

    def tiles(self):
        previous_tile = None
        remaining_scroll = self._total_height
        while remaining_scroll > 0:
            tile = self._get_next_tile(remaining_scroll, previous_tile)
            yield tile
            previous_tile = tile
            remaining_scroll -= previous_tile.height

    def _get_next_tile(self, remaining_scroll, previous_tile):
        if not previous_tile:
            return self._get_first_tile()
        elif self._is_last_tile(remaining_scroll):
            return self._get_last_tile(remaining_scroll, previous_tile)
        else:
            return self._get_intermediate_tile(previous_tile)

    def _get_first_tile(self):
        tile_height = self._max_tile_height
        return self._build_tile(0, tile_height)

    def _build_tile(self, top, height, margin=0):
        return ElementPortion(self._element, (0, top), (self._width, height), (0, margin))

    def _is_last_tile(self, remaining_scroll):
        return remaining_scroll <= self._max_tile_height

    def _get_last_tile(self, remaining_scroll, previous_tile):
        offset = self._get_next_tile_offset(previous_tile)
        height = remaining_scroll
        margin = self._max_tile_height - height
        return self._build_tile(offset, height, margin)

    def _get_next_tile_offset(self, previous_tile):
        return previous_tile.bottom +1

    def _get_intermediate_tile(self, previous_tile):
        offset = self._get_next_tile_offset(previous_tile)
        height = self._max_tile_height
        return self._build_tile(offset, height)


class ElementPortion(object):

    def __init__(self, element, element_offset, size, margin):
        self._element = element
        self._content = Rectangle.from_corner_and_size(element_offset, size)
        self._margin = RectSize(*margin)

    @property
    def element_offset(self):
        return self._content.upper_left_corner

    @property
    def size(self):
        return self._content.size

    @property
    def height(self):
        return self._content.height

    @property
    def bottom(self):
        return self._content.bottom

    @property
    def margin(self):
        return self._margin

    def scroll_into_view(self):
        in_view_position = self.element_offset - self._margin
        self._element.scroll.to(*in_view_position)
        has_scrolled = lambda: self._element.scroll.level == in_view_position
        try:
            Wait(2, poll_frequency=0.01).until(has_scrolled)
        except TimeoutException:
            pass
        assert_that(self._element.scroll.level, equal_to(in_view_position))
