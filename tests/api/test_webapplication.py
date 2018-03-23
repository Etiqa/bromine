import pytest

from bromine import WebApplication, WebPage
from bromine.exceptions import NoSuchPageError


@pytest.fixture(name='app')
def app_fixture():
    class MyWebApp(WebApplication):
        def _add_pages(self):
            self.add_page(WebPage('/some/page', name='some page'))
    app = MyWebApp('https://www.example.com', object())
    return app


def test_base_url(app):
    assert app.base_url == 'https://www.example.com'


def test_browser(app):
    assert hasattr(app, 'browser')


def test_get_page(app):
    assert app.get_page('some page') is not None


def test_registered_page_url(app):
    assert app.get_page('some page').url == 'https://www.example.com/some/page'


def test_registered_page_browser(app):
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


def test_add_page_without_name(app):
    with pytest.raises(ValueError):
        app.add_page(WebPage('/page/without/name'))


def test_duplicated_page_name_error(app):
    with pytest.raises(ValueError):
        app.add_page(WebPage('/another/page', name='some page'))
