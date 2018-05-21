import pytest
from bromine import WebApplication, WebPage

# pylint: disable=line-too-long
@pytest.mark.parametrize('base_url,page_url,expected', (
    ('http://www.example.com', 'some/relative/path', 'http://www.example.com/some/relative/path'),
    ('http://www.example.com', '/some/absolute/path', 'http://www.example.com/some/absolute/path'),
    ('http://www.example.com', '//other.domain.com/some/path', 'http://other.domain.com/some/path'),
    ('http://www.example.com', 'https://other.domain.com/some/path', 'https://other.domain.com/some/path'),
    pytest.mark.xfail(reason='relative url')(
        ('http://www.example.com', 'other.domain.com/some/path', 'http://other.domain.com/some/path')
    ),
    pytest.mark.xfail(reason='relative url')(
        ('www.example.com', 'some/relative/path', 'www.example.com/some/relative/path')
    ),
    pytest.mark.xfail(reason='relative url')(
        ('www.example.com', '/some/absolute/path', 'www.example.com/some/absolute/path')
    ),
    ('www.example.com', '//other.domain.com/some/path', '//other.domain.com/some/path'),
    ('www.example.com', 'https://other.domain.com/some/path', 'https://other.domain.com/some/path'),
    ('www.example.com', 'other.domain.com/some/path', 'other.domain.com/some/path')
))
def test_full_page_url(base_url, page_url, expected):
    app = WebApplication(base_url, None)
    page = WebPage(app, page_url)
    assert page.url() == expected
