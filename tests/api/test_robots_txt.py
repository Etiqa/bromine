from textwrap import dedent

import pytest

from bromine.utils.robots_txt import RobotsTxt

from .. import Mock, patch


@pytest.fixture(name='setup_robots_file')
def fixture_impl():
    def apply_config(patched_requests_module):
        status_code = 200
        robots_txt = dedent("""\
            User-agent: *
            Disallow: /secret

            Sitemap: https://www.example.com/sitemap.xml
        """)
        mocked_response = Mock()
        mocked_response.status_code = status_code
        mocked_response.text = robots_txt
        patched_requests_module.get.return_value = mocked_response
    return apply_config


def test_status_code(setup_robots_file):
    with patch('bromine.utils.robots_txt.requests') as mocked_requests:
        setup_robots_file(mocked_requests)

        rbt = RobotsTxt('https://www.example.com')
        assert rbt.status_code == 200


def test_directives(setup_robots_file):
    with patch('bromine.utils.robots_txt.requests') as mocked_requests:
        setup_robots_file(mocked_requests)

        rbt = RobotsTxt('https://www.example.com')
        assert rbt.directives == (
            ('User-agent', '*'),
            ('Disallow', '/secret'),
            '',
            ('Sitemap', 'https://www.example.com/sitemap.xml')
        )
