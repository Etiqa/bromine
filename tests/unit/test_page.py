import pytest
from selenium.webdriver import Remote as SeWebDriver

from bromine import WebApplication, WebPage

from .. import Mock, PropertyMock


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


def test_page_title_proxies_browser_title(): # pylint: disable=invalid-name
    browser = Mock(spec=SeWebDriver)
    mocked_title = PropertyMock(return_value='some value')
    type(browser).title = mocked_title
    app = WebApplication('https://www.example.com', browser)
    page = WebPage(app, '/some/page')
    assert page.title == 'some value'
    mocked_title.assert_called_once()


@pytest.mark.skip(reason="not implemented") # TODO: write implementation
class TestGoTo(object):

    def test_go_to_calls_browser_get(self):
        raise NotImplementedError

    def test_go_to_assertion(self):
        raise NotImplementedError

    def test_go_to_assertion_error(self):
        raise NotImplementedError


@pytest.mark.skip(reason="not implemented") # TODO: write implementation
class TestIsCurrentPage(object):

    def test_current_url(self):
        raise NotImplementedError
