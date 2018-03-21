import pytest

from bromine import WebPage


@pytest.fixture(name='page')
def page_fixture():
    page = WebPage('https://www.example.com/some/page')
    return page


def test_url(page):
    assert page.url == 'https://www.example.com/some/page'


def test_set_url(page):
    some_other_url = '/some/other/url'
    page.url = some_other_url
    assert page.url == some_other_url


def test_browser(page):
    assert page.browser is None


def test_set_browser(page):
    page.browser = object()
    assert page.browser is not None


def test_optional_browser():
    browser = object()
    page = WebPage('https://www.example.com/some/page', browser=browser)
    assert page.browser is browser


def test_name(page):
    assert page.name is None


def test_optional_name():
    page = WebPage('https://www.example.com/some/page', name='some page')
    assert page.name == 'some page'


def test_name_is_readonly(page):
    with pytest.raises(AttributeError, message="can't set attribute"):
        page.name = 'some page'


def test_add_elements():
    class MyPage(WebPage):
        def _add_elements(self):
            self.some_element = None
    page = MyPage('/some/page')
    assert hasattr(page, 'some_element')
