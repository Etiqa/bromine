from collections import namedtuple

from bromine.exceptions import (NoSuchElementException,
                                MultipleElementsFoundError,
                                StaleElementReferenceException)


class Element(object):
    """Represents a UI component inside a View."""


class WebElement(Element):
    """Represents a web element inside a web page.

    Wraps a Selenium WebElement and adds auto-refreshing behaviour
    to avoid StaleElementReferenceException's
    """

    Locator = namedtuple('Locator', ('by', 'path'))

    def __init__(self, browser, path, find_by='xpath'):
        self._locator = WebElement.Locator(find_by, path)
        self._browser = browser
        self._dom_element = None

    @property
    def dom_element(self):
        if self._dom_element is None:
            self._find_dom_element()
        return self._dom_element

    def _find_dom_element(self):
        find_method = 'find_elements_by_{}'.format(self._locator.by)
        find = getattr(self._browser, find_method)
        found_elements = find(self._locator.path)
        if not found_elements:
            raise NoSuchElementException(self._locator)
        elif len(found_elements) > 1:
            raise MultipleElementsFoundError(self._locator)
        else:
            element = found_elements[0]
            assert element is not None
            self._dom_element = element

    def is_present(self):
        try:
            self._find_dom_element()
        except NoSuchElementException:
            return False
        else:
            return True

    def is_displayed(self):
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
        if not callable(attr):
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
