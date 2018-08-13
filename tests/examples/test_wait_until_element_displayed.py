import pytest

from selenium.webdriver import Remote as SeWebDriver

from bromine import WebElement
from bromine.element.locator import Locator
from bromine.exceptions import TimeoutException
from bromine.utils.wait import Wait

from .. import Mock


def test_wait_until_displayed(appearing_element):
    assert not appearing_element.is_displayed()
    Wait(1, poll_frequency=0.01).until(appearing_element.is_displayed)
    assert appearing_element.is_displayed()
    assert appearing_element.dom_element.is_displayed.call_count == 4


def test_wait_until_displayed_timeout(hidden_element):
    assert not hidden_element.is_displayed()
    with pytest.raises(TimeoutException):
        Wait(0.1, poll_frequency=0.01).until(hidden_element.is_displayed)
    assert hidden_element.dom_element.is_displayed.call_count >= 2


@pytest.fixture(name='appearing_element')
def appearing_element_fixture(web_element):
    web_element.dom_element.is_displayed.side_effect = [False, False, True, True]
    return web_element


@pytest.fixture(name='hidden_element')
def hidden_element_fixture(web_element):
    web_element.dom_element.is_displayed.return_value = False
    return web_element


@pytest.fixture(name='web_element')
def web_element_fixture():
    browser = Mock(spec=SeWebDriver)
    dom_element = Mock()
    locator = Mock(spec=Locator, return_value=[dom_element])
    return WebElement(browser, locator)
