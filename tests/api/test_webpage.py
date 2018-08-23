import pytest

from selenium.webdriver import Remote as SeWebDriver

from bromine import WebPage

from .. import Mock, PropertyMock


@pytest.fixture(name='page')
def page_fixture():
    browser = Mock(spec=SeWebDriver)
    page = WebPage('https://www.example.com/some/page', browser)
    return page


@pytest.fixture(name='different_url')
def different_url_fixture(page):
    different_url = page.url.replace('some', 'another')
    assert different_url != page.url
    return different_url


def test_url(page):
    assert page.url == 'https://www.example.com/some/page'


def test_browser(page):
    assert page.browser is not None


def test_title(page):
    _mock_browser_property(page.browser, 'title', 'some title')
    assert page.title == 'some title'


def test_go_to(page):
    assert not page.is_current_page()
    _mock_browser_get(page.browser, page.url)
    page.go_to()
    assert page.is_current_page()


def test_go_to_does_not_assert_current_page(page, different_url):
    _mock_browser_get(page.browser, different_url)
    page.go_to()
    assert not page.is_current_page()


def test_is_current_page(page):
    _mock_browser_property(page.browser, 'current_url', page.url)
    assert page.is_current_page()


def test_is_not_current_page(page, different_url):
    _mock_browser_property(page.browser, 'current_url', different_url)
    assert not page.is_current_page()


@pytest.mark.skip(reason="TODO: this test has not been implemented yet") # TODO: write test
def test_size(page):
    size = page.size
    assert hasattr(size, 'total')
    assert hasattr(size, 'visible')
    assert isinstance(size, type(page).size) # this is to test accessing size from Page class


def _mock_browser_property(browser, key, value):
    setattr(type(browser), key, PropertyMock(return_value=value))


def _mock_browser_get(browser, final_url):
    mock_current_url = lambda *_: _mock_browser_property(browser, 'current_url', final_url)
    browser.get.side_effect = mock_current_url
