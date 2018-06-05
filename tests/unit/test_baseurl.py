import pytest
from bromine import WebApplication, Environment


test_base_urls = ( # pylint: disable=invalid-name
    'https://www.example.com',
    'http://www.example.com',
    '//www.example.com',
    pytest.mark.xfail(reason='relative url')('www.example.com'),
)


@pytest.mark.parametrize('base_url', test_base_urls)
def test_base_url(base_url):
    app = WebApplication(Environment(base_url), None)
    assert app.base_url() == base_url


@pytest.mark.parametrize('base_url', test_base_urls)
def test_get_https_base_url(base_url):
    app = WebApplication(Environment(base_url), None)
    assert app.base_url('https') == 'https://www.example.com'


@pytest.mark.parametrize('base_url', test_base_urls)
def test_get_http_base_url(base_url):
    app = WebApplication(Environment(base_url), None)
    assert app.base_url('http') == 'http://www.example.com'
