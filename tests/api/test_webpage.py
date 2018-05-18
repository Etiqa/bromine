import pytest

from bromine import WebPage, WebApplication


@pytest.fixture(name='page')
def page_fixture():
    page = WebPage('/some/page')
    page.application = WebApplication('https://www.example.com', object())
    return page


def test_url(page):
    assert page.url() == 'https://www.example.com/some/page'


def test_https_url(page):
    assert page.url('https') == 'https://www.example.com/some/page'


def test_http_url(page):
    assert page.url('http') == 'http://www.example.com/some/page'


def test_browser(page):
    assert page.browser is page.application.browser


def test_default_name(page):
    assert page.name is None


def test_name():
    page = WebPage('https://www.example.com/some/page', name='some page')
    assert page.name == 'some page'


def test_name_is_readonly(page):
    with pytest.raises(AttributeError, message="can't set attribute"):
        page.name = 'some page'


def test_add_elements():
    class MyPage(WebPage):
        def _add_elements(self):
            self.some_element = object()
    page = MyPage('/some/page')
    assert hasattr(page, 'some_element')
