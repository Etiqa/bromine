import pytest

from bromine.utils.url import http, https


input_urls = pytest.mark.parametrize('url', (  # pylint: disable=invalid-name
    'http://www.example.com/',
    'https://www.example.com/',
    '//www.example.com/',
    pytest.mark.xfail(reason='url is not absolute')('www.example.com/')
))


@input_urls
def test_http_scheme(url):
    assert http(url) == 'http://www.example.com/'


@input_urls
def test_https_scheme(url):
    assert https(url) == 'https://www.example.com/'
