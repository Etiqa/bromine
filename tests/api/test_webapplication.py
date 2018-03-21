import pytest

from bromine import WebApplication, WebPage
from bromine.exceptions import NoSuchPageError


@pytest.fixture(name='app')
def app_fixture():
    app = WebApplication('https://www.example.com', object())
    app.pages = [
        WebPage('/some/page', name='some page')
    ]
    return app


def test_base_url(app):
    assert app.base_url == 'https://www.example.com'


def test_browser(app):
    assert hasattr(app, 'browser')


def test_get_page(app):
    assert app.get_page('some page') is not None


def test_page_url(app):
    assert app.get_page('some page').url == 'https://www.example.com/some/page'


def test_page_browser(app):
    assert app.get_page('some page').browser is app.browser


def test_get_unregistered_page(app):
    with pytest.raises(NoSuchPageError):
        app.get_page('some unregistered page')


def test_initial_current_page(app):
    assert app.current_page is None


def test_current_page(app):
    page = app.get_page('some page')
    app.current_page = page
    assert app.current_page is page


def test_current_page_must_be_registered(app): #pylint: disable=invalid-name
    with pytest.raises(NoSuchPageError):
        app.current_page = WebPage('/unregistered', None)


def test_adding_page_without_name():
    with pytest.raises(AssertionError):
        WebApplication('', None).pages = [
            WebPage('/page/without/name')
        ]


def test_adding_two_pages_with_the_same_name():
    with pytest.raises(AssertionError):
        WebApplication('', None).pages = [
            WebPage('/some/page', name='some name'),
            WebPage('/another/page', name='some name')
        ]
