from hamcrest import assert_that, equal_to

from bromine.utils.geometry import Rectangle, RectSize
from bromine.utils.wait import Wait
from selenium.common.exceptions import TimeoutException


class SimpleVerticalLayout(object):

    def __init__(self, page):
        total_width, total_height = page.size
        visible_width, visible_height = page.visible_size
        window = page.browser.window
        assert total_width == visible_width
        self._page = page
        self._window = window
        self._width = total_width
        self._total_height = total_height
        self._max_tile_height = visible_height
        self._address_bar_height = window.address_bar_height
        self._bar_shadow_height = window.bar_shadow_height

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
        if self._total_height <= self._max_tile_height:
            tile_height = self._max_tile_height
        else:
            tile_height = self._max_tile_height - self._bar_shadow_height
        return self._build_tile(0, 0, tile_height)

    def _build_tile(self, top_margin, top, height):
        return PagePortion(self._page, (0, top), (self._width, height), (0, top_margin))

    def _is_last_tile(self, remaining_scroll):
        return remaining_scroll <= self._max_tile_height - self._bar_shadow_height

    def _get_last_tile(self, remaining_scroll, previous_tile):
        offset = self._get_next_tile_offset(previous_tile)
        height = remaining_scroll
        margin = self._max_tile_height - height
        return self._build_tile(margin, offset, height)

    def _get_next_tile_offset(self, previous_tile):
        return previous_tile.bottom +1

    def _get_intermediate_tile(self, previous_tile):
        offset = self._get_next_tile_offset(previous_tile)
        height = self._max_tile_height - 2*self._bar_shadow_height
        margin = self._bar_shadow_height
        return self._build_tile(margin, offset, height)


class PagePortion(object):

    def __init__(self, page, page_offset, size, margin):
        self._page = page
        self._content = Rectangle.from_corner_and_size(page_offset, size)
        self._margin = RectSize(*margin)

    @property
    def page_offset(self):
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
        in_view_position = self.page_offset - self._margin
        self._page.scroll.to(*in_view_position)
        has_scrolled = lambda: self._page.scroll.level == in_view_position
        try:
            Wait(2, poll_frequency=0.01).until(has_scrolled)
        except TimeoutException:
            pass
        assert_that(self._page.scroll.level, equal_to(in_view_position))
