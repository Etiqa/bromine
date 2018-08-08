import pytest

from bromine import WebApplication


@pytest.fixture(name='app')
def app_fixture():
    app = WebApplication('https://www.example.com', object())
    return app


def test_base_url(app):
    assert app.base_url == 'https://www.example.com'


def test_browser(app):
    assert hasattr(app, 'browser')


def test_initial_current_page(app):
    assert app.current_page is None


def test_current_page(app):
    page = object()
    app.current_page = page
    assert app.current_page is page
