import pytest

from selenium.webdriver import Remote as SeWebDriver

from bromine import WebPage, WebApplication, WebElement

from .. import Mock, PropertyMock


@pytest.fixture(name='page')
def page_fixture():
    browser = Mock(spec=SeWebDriver)
    app = WebApplication('https://www.example.com', browser)
    page = WebPage(app, '/some/page')
    return page


def test_url(page):
    assert page.url() == 'https://www.example.com/some/page'


def test_https_url(page):
    assert page.url('https') == 'https://www.example.com/some/page'


def test_http_url(page):
    assert page.url('http') == 'http://www.example.com/some/page'


def test_relative_url(page):
    assert page.relative_url == '/some/page'


def test_browser(page):
    assert page.browser is page.application.browser


def test_default_name_is_relative_url(page): # pylint: disable=invalid-name
    assert page.name == '/some/page'


def test_name():
    page = WebPage(None, 'https://www.example.com/some/page', name='some page')
    assert page.name == 'some page'


def test_name_is_readonly(page):
    with pytest.raises(AttributeError, match="can't set attribute"):
        page.name = 'some page'


def test_add_elements():
    class MyPage(WebPage):
        def _add_elements(self):
            self.some_element = WebElement(self.browser, '')
    app = WebApplication('https://www.example.com', object())
    page = MyPage(app, '/some/page')
    assert page.some_element._browser is page.browser # pylint: disable=protected-access


def test_title(page):
    mocked_title = PropertyMock(return_value='some title')
    type(page.browser).title = mocked_title
    assert page.title == 'some title'


def test_go_to(page):
    assert hasattr(page, 'go_to')


def test_is_current_page(page):
    assert hasattr(page, 'is_current_page')
