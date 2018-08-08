from textwrap import dedent

import pytest

from bromine.utils.robots_txt import RobotsTxt

from .. import Mock, patch


@pytest.fixture(name='robots_txt')
def robots_txt_fixture():
    robots_txt = Mock()
    robots_txt.status_code = 200
    robots_txt.text = dedent("""\
        User-agent: *
        Disallow: /secret

        Sitemap: https://www.example.com/sitemap.xml
    """)
    return robots_txt


def test_status_code(robots_txt):
    with patch('bromine.utils.robots_txt.requests') as mocked_requests:
        mocked_requests.get.return_value = robots_txt

        rbt = RobotsTxt('https://www.example.com')
        assert rbt.status_code == 200


def test_directives(robots_txt):
    with patch('bromine.utils.robots_txt.requests') as mocked_requests:
        mocked_requests.get.return_value = robots_txt

        rbt = RobotsTxt('https://www.example.com')
        assert rbt.directives == (
            ('User-agent', '*'),
            ('Disallow', '/secret'),
            '',
            ('Sitemap', 'https://www.example.com/sitemap.xml')
        )
