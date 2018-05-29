"""
Web element model.
"""

import six

from bromine.exceptions import (NoSuchElementException,
                                MultipleElementsFoundError,
                                StaleElementReferenceException)
from .base import Element
from .locator import Locator, XPath


class WebElement(Element):
    """Represents a web element inside a web page.

    Wraps a Selenium WebElement and adds auto-refreshing behaviour
    to avoid StaleElementReferenceException's
    """

    def __init__(self, browser, locator, dom_element=None):
        if not isinstance(locator, Locator):
            if not isinstance(locator, six.string_types):
                raise TypeError('locator must be a Locator instance or a XPath string')
            locator = XPath(locator)
        self._locator = locator
        self._browser = browser
        self._dom_element = dom_element
        # TODO: consistency check: dom_element's driver is self._browser

    @property
    def dom_element(self):
        """Underlying Selenium WebElement object."""
        if self._dom_element is None:
            self._find_dom_element()
        return self._dom_element

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

    # def is_displayed(self, timeout_milliseconds=None, wait_for_animation=False):
    #     if timeout_milliseconds is None:
    #         timeout_milliseconds = self._display_timeout_milliseconds
    #
    #     if wait_for_animation:
    #         time.sleep(self._animation_timeout_milliseconds / 1000.0)
    #
    #     displayed = self._is_displayed()
    #
    #     wait_iterations = int(math.floor(timeout_milliseconds / self.POLL_PERIOD_MILLISEC))
    #     poll_period_sec = self.POLL_PERIOD_MILLISEC / 1000.0
    #     while (not displayed) and (wait_iterations > 0):
    #         wait_iterations -= 1
    #         time.sleep(poll_period_sec)
    #         # in a Selenium Grid environment self._is_displayed() duration
    #         # has a significant impact that needs to be taken into account
    #         start = datetime.now()
    #         displayed = self._is_displayed()
    #         end = datetime.now()
    #         duration_millisec = (end - start).total_seconds() * 1000
    #         correction = int(math.floor(duration_millisec / self.POLL_PERIOD_MILLISEC))
    #         if correction > 0:
    #             wait_iterations -= correction
    #
    #     return displayed
    #
    # def move_to_element(self):
    #     to_perform = ActionChains(self.driver).move_to_element(self.web_element)
    #     to_perform.perform()
    #
    # def double_click(self):
    #     actions = ActionChains(self.driver)
    #     actions.double_click(self.web_element)
    #     actions.perform()
    #
    # def click(self):
    #     try:
    #         self.web_element.click()
    #     except WebDriverException as e:
    #         if re.search(r'Element.* is not clickable at point \(.*, .*\)\. Other element would receive the click', e.msg):
    #             self.driver.execute_script("arguments[0].scrollIntoView(false);", self.web_element)
    #             try:
    #                 self.web_element.click()
    #             except WebDriverException as e2:
    #                 if re.search(r'Element.* is not clickable at point \(.*, .*\)\. Other element would receive the click', e2.msg):
    #                     self.driver.execute_script("arguments[0].scrollIntoView(true);", self.web_element)
    #                     self.web_element.click()
    #                 else:
    #                     raise
    #         else:
    #             raise


# TODO: DOC: elements array must not change during iteration
class ElementCollection(object):

    def __init__(self, browser, locator, element_factory=WebElement):
        self._locator = locator
        self._browser = browser
        self._element_factory = element_factory

    def __iter__(self):
        dom_elements = self._locator.find_elements(self._browser)
        return (self._instantiate_item(i, el) for i, el in enumerate(dom_elements))

    def _instantiate_item(self, index, dom_element):
        return self._element_factory(self._browser, self._locator.item(index), dom_element)
