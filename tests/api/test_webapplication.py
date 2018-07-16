import pytest

from bromine import WebApplication, Environment, WebPage
from bromine.exceptions import NoSuchPageError
from bromine.utils.robots_txt import RobotsTxt


@pytest.fixture(name='app')
def app_fixture():
    class MyWebApp(WebApplication):
        def _add_pages(self):
            self.add_page(WebPage(self, '/some/page', name='some page'))
    app = MyWebApp(Environment('https://www.example.com'), object())
    return app


def test_base_url(app):
    assert app.base_url() == 'https://www.example.com'


def test_get_https_base_url(app):
    assert app.base_url('https') == 'https://www.example.com'


def test_get_http_base_url(app):
    assert app.base_url('http') == 'http://www.example.com'


def test_browser(app):
    assert hasattr(app, 'browser')


def test_get_page(app):
    assert app.get_page('some page') is not None


def test_registered_page_url(app):
    assert app.get_page('some page').url() == 'https://www.example.com/some/page'


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


def test_current_page_must_be_registered(app): # pylint: disable=invalid-name
    with pytest.raises(NoSuchPageError):
        app.current_page = WebPage(app, '/unregistered', None)


def test_add_page_without_name(app):
    with pytest.raises(ValueError, match="Page's name must not be empty"):
        app.add_page(WebPage(app, '', name=None))


def test_duplicated_page_name_error(app):
    with pytest.raises(ValueError, match='Duplicate name "some page"'):
        app.add_page(WebPage(app, '/another/page', name='some page'))


def test_inconsistent_application_error(app): # pylint: disable=invalid-name
    another_app = WebApplication(None, None)
    with pytest.raises(ValueError, match="Page's application is inconsistent"):
        app.add_page(WebPage(another_app, '/'))


class TestRobotsTxt(object):
    # pylint: disable=no-self-use

    def test_robots_txt(self, app):
        assert isinstance(app.robots_txt(), RobotsTxt)

    @pytest.mark.parametrize('scheme,robots_url', (
        (None, 'https://www.example.com/robots.txt'),
        ('http', 'http://www.example.com/robots.txt'),
        ('https', 'https://www.example.com/robots.txt'),
    ))
    def test_robots_file_url(self, app, scheme, robots_url):
        assert app.robots_txt(scheme).url == robots_url

    def test_robots_txt_extra_params(self, app):
        rbt = app.robots_txt(verify_ssl=False)
        assert rbt.__dict__['_verify_ssl'] is False
