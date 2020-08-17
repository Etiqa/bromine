import pytest
from selenium.webdriver import Remote as SeWebDriver
from bromine.webdriver.window import Window
from .. import Mock




class _BaseWindowTest(object):

    def test_outer_size(self):
        raise NotImplementedError

    def test_inner_size(self):
        raise NotImplementedError

    def test_virtual_pixel_ratio(self):
        raise NotImplementedError

    def test_physical_pixel_ratio(self):
        raise NotImplementedError

    def test_screenshot(self):
        raise NotImplementedError

@pytest.fixture(name='browser')
def browser_fixture():
    browser = Mock(spec=SeWebDriver)
    return browser

def test_address_bar_height_default(browser):
    browser.window = Window(browser)
    assert browser.window.address_bar_height == 0

def test_address_bar_height_10(browser):
    browser.address_bar_height = 10
    browser.window = Window(browser)
    assert browser.window.address_bar_height == 10

def test_bar_shadow_height_default(browser):
    browser.window = Window(browser)
    assert browser.window.bar_shadow_height == 0

def test_bar_shadow_height_10(browser):
    browser.bar_shadow_height = 10
    browser.window = Window(browser)
    assert browser.window.bar_shadow_height == 10

@pytest.mark.skip(reason="TODO: this test has not been implemented yet") # TODO: write test
class TestWindow(_BaseWindowTest):
        
    def test_outer_size_is_readonly(self):
        raise NotImplementedError
    
    def test_inner_size_is_readonly(self):
        raise NotImplementedError


@pytest.mark.skip(reason="TODO: this test has not been implemented yet") # TODO: write test
class TestResizableWindow(_BaseWindowTest):

    def test_outer_size_can_be_modified(self):
        raise NotImplementedError

    def test_inner_size_can_be_modified(self):
        raise NotImplementedError

    def test_maximize(self):
        raise NotImplementedError
