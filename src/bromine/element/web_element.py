"""
Web element model.
"""

import six

from bromine.exceptions import (NoSuchElementException,
                                MultipleElementsFoundError,
                                StaleElementReferenceException)
from .base import Element
from .locator import Locator, XPath
from ..utils.image import ScreenshotFromPngBytes
from .scroll import ElementScroller
from .size import Html5ElementSize
from .layout import SimpleVerticalLayout


class WebElement(Element):
    """Represents a web element inside a web page.

    Wraps a Selenium WebElement and adds auto-refreshing behaviour
    to avoid StaleElementReferenceException's
    """
    _size = Html5ElementSize

    def __init__(self, browser, locator, dom_element=None):
        if not isinstance(locator, Locator):
            if not isinstance(locator, six.string_types):
                raise TypeError('locator must be a Locator instance or a XPath string')
            locator = XPath(locator)
        self._locator = locator
        self._browser = browser
        self._dom_element = dom_element
        self._size = self.__class__._size(self)

        # TODO: consistency check: dom_element's driver is self._browser

    @property
    def dom_element(self):
        """Underlying Selenium WebElement object."""
        if self._dom_element is None:
            self._find_dom_element()
        return self._dom_element
    
    @property
    def browser(self):
        """Instance of Selenium WebDriver."""
        return self._browser

    @property
    def scroll(self):
        return ElementScroller(self)

    @property
    def scroll_size(self):
        return self._size.scroll_size()

    @property
    def size(self):
        return self._size.size()

    @property
    def layout(self):
        return SimpleVerticalLayout(self)

    def _find_dom_element(self):
        found_elements = self._locator(self._browser)
        if not found_elements:
            raise NoSuchElementException(self._locator)
        elif len(found_elements) > 1:
            raise MultipleElementsFoundError(self._locator)
        else:
            element = found_elements[0]
            assert element is not None
            self._dom_element = element

    def is_present(self):
        """Test whether this element is attached to the DOM."""
        try:
            self._find_dom_element()
        except NoSuchElementException:
            return False
        else:
            return True

    def is_displayed(self):
        """Test whether this element is displayed.

        This method invokes is_displayed() method of the underlying
        dom_element.
        If the underlying dom_element is stale, it is automatically
        refreshed.
        If dom_element is not present, this method returns False
        instead of raising NoSuchElementException.
        """
        try:
            return self.dom_element.is_displayed()
        except NoSuchElementException:
            return False
        except StaleElementReferenceException:
            try:
                self._find_dom_element()
                return self.dom_element.is_displayed()
            except NoSuchElementException:
                return False

    def __getattr__(self, name):
        try:
            attr = getattr(self.dom_element, name)
        except StaleElementReferenceException:
            self._find_dom_element()
            attr = getattr(self.dom_element, name)
        if not callable(attr): # pylint: disable=no-else-return
            return attr
        else:
            def auto_refresh_wrapper(*args, **kwargs):
                try:
                    return attr(*args, **kwargs)
                except StaleElementReferenceException:
                    self._find_dom_element()
                    return getattr(self.dom_element, name)(*args, **kwargs)
            return auto_refresh_wrapper

    def get_screenshot(self):
        """Return ScreenshotFromPngBytes object.
        """
        png_bytes = self._dom_element.screenshot_as_png
        return ScreenshotFromPngBytes(png_bytes)

# TODO: DOC: elements array must not change during iteration
class ElementCollection(object):

    def __init__(self, browser, locator, element_factory=WebElement):
        if not isinstance(locator, Locator):
            if not isinstance(locator, six.string_types):
                raise TypeError('locator must be a Locator instance or a XPath string')
            locator = XPath(locator)
        self._locator = locator
        self._browser = browser
        self._element_factory = element_factory

    def __iter__(self):
        dom_elements = self._locator(self._browser)
        return (self._instantiate_item(i, el) for i, el in enumerate(dom_elements))

    def _instantiate_item(self, index, dom_element):
        return self._element_factory(self._browser, self._locator.item(index), dom_element)
