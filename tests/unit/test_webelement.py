# pylint: disable=wrong-import-position,invalid-name,no-self-use,too-few-public-methods

import pytest
import six
if six.PY3:
    from unittest.mock import Mock, PropertyMock
else:
    from mock import Mock, PropertyMock # pylint: disable=import-error

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webdriver import WebElement as SeWebElement

from bromine import WebElement
from bromine.exceptions import (NoSuchElementException,
                                MultipleElementsFoundError,
                                StaleElementReferenceException)


@pytest.fixture(name='browser')
def webdriver_mock():
    mock = Mock(spec=WebDriver)
    mock.find_elements_by_xpath.side_effect = lambda self: [Mock(spec=SeWebElement)]
    return mock


@pytest.fixture(name='displayed_dom_element')
def displayed_dom_element_mock():
    mock = Mock(spec=SeWebElement)
    mock.is_displayed.return_value = True
    return mock


@pytest.fixture(name='hidden_dom_element')
def hidden_dom_element_mock():
    mock = Mock(spec=SeWebElement)
    mock.is_displayed.return_value = False
    return mock


@pytest.fixture(name='stale_dom_element')
def stale_dom_element_mock():
    mock = Mock(spec=SeWebElement)
    mock.is_displayed = Mock(side_effect=StaleElementReferenceException)
    return mock


def test_loading_dom_element_for_the_first_time(browser):
    el = WebElement(browser, "some_tag[@some_attr='some_value']")
    el._find_dom_element = Mock(wraps=el._find_dom_element) # pylint: disable=protected-access
    dom_el = el.dom_element
    assert dom_el is not None
    el._find_dom_element.assert_called_once() # pylint: disable=protected-access


def test_subsequent_accesses_to_dom_element_use_cached_object(browser):
    el = WebElement(browser, "some_tag[@some_attr='some_value']")
    el._find_dom_element = Mock(wraps=el._find_dom_element) # pylint: disable=protected-access
    dom_el = el.dom_element
    assert el.dom_element is dom_el
    el._find_dom_element.assert_called_once() # pylint: disable=protected-access


def test_no_such_element_exception(browser):
    browser.find_elements_by_xpath = Mock(return_value=[])
    el = WebElement(browser, "some_tag[@some_attr='some_value']")
    with pytest.raises(NoSuchElementException):
        el.dom_element # pylint: disable=pointless-statement


def test_multiple_elements_exception(browser):
    browser.find_elements_by_xpath = Mock(return_value=[object(), object()])
    el = WebElement(browser, "some_tag[@some_attr='some_value']")
    with pytest.raises(MultipleElementsFoundError):
        el.dom_element # pylint: disable=pointless-statement


def test_is_present(browser):
    el = WebElement(browser, "some_tag[@some_attr='some_value']")
    assert el.is_present()


def test_is_not_present(browser):
    browser.find_elements_by_xpath = Mock(return_value=[])
    el = WebElement(browser, "some_tag[@some_attr='some_value']")
    assert not el.is_present()


def test_is_present_always_refreshes_dom_element(browser):
    el = WebElement(browser, "some_tag[@some_attr='some_value']")
    el._find_dom_element = Mock(wraps=el._find_dom_element) # pylint: disable=protected-access
    dom_el = el.dom_element
    el.is_present()
    assert el.dom_element is not dom_el
    assert el._find_dom_element.call_count == 2 # pylint: disable=protected-access


def test_is_displayed(browser, displayed_dom_element):
    browser.find_elements_by_xpath = Mock(return_value=[displayed_dom_element])
    el = WebElement(browser, "some_tag[@some_attr='some_value']")
    assert el.is_displayed()


def test_is_not_displayed(browser, hidden_dom_element):
    browser.find_elements_by_xpath = Mock(return_value=[hidden_dom_element])
    el = WebElement(browser, "some_tag[@some_attr='some_value']")
    assert not el.is_displayed()


def test_is_displayed_when_stale(browser, stale_dom_element, displayed_dom_element):
    browser.find_elements_by_xpath.side_effect = ([stale_dom_element], [displayed_dom_element])
    el = WebElement(browser, "some_tag[@some_attr='some_value']")
    el._find_dom_element = Mock(wraps=el._find_dom_element) # pylint: disable=protected-access
    assert el.dom_element is stale_dom_element
    assert el.is_displayed()
    assert el.dom_element is displayed_dom_element
    assert el._find_dom_element.call_count == 2 # pylint: disable=protected-access
    stale_dom_element.is_displayed.assert_called_once()
    displayed_dom_element.is_displayed.assert_called_once()


def test_is_not_displayed_when_stale(browser, stale_dom_element, hidden_dom_element):
    browser.find_elements_by_xpath.side_effect = ([stale_dom_element], [hidden_dom_element])
    el = WebElement(browser, "some_tag[@some_attr='some_value']")
    el._find_dom_element = Mock(wraps=el._find_dom_element) # pylint: disable=protected-access
    assert el.dom_element is stale_dom_element
    assert not el.is_displayed()
    assert el.dom_element is hidden_dom_element
    assert el._find_dom_element.call_count == 2 # pylint: disable=protected-access
    stale_dom_element.is_displayed.assert_called_once()
    hidden_dom_element.is_displayed.assert_called_once()


def test_is_not_displayed_when_dom_element_is_not_present(browser):
    browser.find_elements_by_xpath = Mock(return_value=[])
    el = WebElement(browser, "some_tag[@some_attr='some_value']")
    assert not el.is_displayed()


def test_is_not_displayed_when_dom_element_is_stale_and_no_more_present(browser, stale_dom_element):
    browser.find_elements_by_xpath.side_effect = ([stale_dom_element], [])
    el = WebElement(browser, "some_tag[@some_attr='some_value']")
    el._find_dom_element = Mock(wraps=el._find_dom_element) # pylint: disable=protected-access
    assert el.dom_element is stale_dom_element
    assert not el.is_displayed()
    assert el._find_dom_element.call_count == 2 # pylint: disable=protected-access
    stale_dom_element.is_displayed.assert_called_once()


def test_proxies_access_to_dom_element(browser):
    class DomElementMock(object):
        @property
        def some_property(self):
            return 'some value'
        def some_method(self, x):
            return x
    dom_element_mock = DomElementMock()
    browser.find_elements_by_xpath = Mock(return_value=[dom_element_mock])

    el = WebElement(browser, "some_tag[@some_attr='some_value']")
    assert el.some_property == 'some value'
    assert el.some_method('some other value') == 'some other value'


def test_refreshes_dom_element_on_property_access_when_stale(browser):
    class DomElementMock(object):
        @property
        def some_property(self):
            return 'some value'
    dom_element_mock = DomElementMock()
    stale_element_mock = Mock(spec=DomElementMock)
    property_mock = PropertyMock(side_effect=StaleElementReferenceException)
    type(stale_element_mock).some_property = property_mock
    browser.find_elements_by_xpath.side_effect = ([stale_element_mock], [dom_element_mock])

    el = WebElement(browser, "some_tag[@some_attr='some_value']")
    assert el.dom_element is stale_element_mock
    assert el.some_property == 'some value'
    assert el.dom_element is dom_element_mock


def test_refreshes_dom_element_on_method_call_when_stale(browser):
    class DomElementMock(object):
        def some_method(self, x):
            return x
    dom_element_mock = DomElementMock()
    stale_element_mock = Mock(spec=DomElementMock)
    stale_element_mock.some_method = Mock(side_effect=StaleElementReferenceException)
    browser.find_elements_by_xpath.side_effect = ([stale_element_mock], [dom_element_mock])

    el = WebElement(browser, "some_tag[@some_attr='some_value']")
    assert el.dom_element is stale_element_mock
    assert el.some_method('some value') == 'some value'
    assert el.dom_element is dom_element_mock
