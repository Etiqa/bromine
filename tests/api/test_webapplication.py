import pytest

from bromine import WebApplication
from bromine.exceptions import NoSuchPageError


@pytest.fixture(name='app')
def app_fixture():
    app = WebApplication('https://www.example.com/some/base/path', None)
    app.add_page('some page', None)
    return app


def test_add_page(app):
    page = None
    app.add_page('some other page', page)
    assert app.get_page('some other page') is page


def test_get_unregistered_page(app):
    with pytest.raises(NoSuchPageError):
        app.get_page('some unregistered page')


def test_replace_page(app):
    previous_page = app.get_page('some page')
    app.add_page('some page', {})
    assert app.get_page('some page') is not previous_page


def test_current_page_unset(app):
    assert app.current_page is None


def test_current_page(app):
    page = app.get_page('some page')
    app.current_page = page
    assert app.current_page is page


def test_current_page_must_be_registered(app): #pylint: disable=invalid-name
    with pytest.raises(NoSuchPageError):
        app.current_page = {}


def test_base_url(app):
    assert app.base_url == 'https://www.example.com/some/base/path'


def test_browser(app):
    assert hasattr(app, 'browser')
