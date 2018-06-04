from textwrap import dedent

import pytest

from bromine.utils.robots_txt import RobotsTxt


@pytest.mark.parametrize('line,field,value', (
    ('Field: value', 'Field', 'value'),
    ('Field:value', 'Field', 'value'),
    ('Field : value', 'Field', 'value'),
    ('\t Field with spaces : \t value with spaces \t', 'Field with spaces', 'value with spaces'),
    ('Field: value:with:colons', 'Field', 'value:with:colons'),
    ('Field: # empty value', 'Field', ''),
))
def test_split_directive(line, field, value):
    expected = (
        (field, value),
    )
    assert RobotsTxt.parse_directives(line) == expected


def test_invalid_lines_are_ignored():
    text = dedent("""\
        Directive1: value1
        Invalid_directive
        Directive2: value2
    """)
    assert RobotsTxt.parse_directives(text) == (
        ('Directive1', 'value1'),
        ('Directive2', 'value2'),
    )


def test_parse_empty_line():
    text = dedent("""\
        Directive1: value1

        Directive2: value2
    """)
    assert RobotsTxt.parse_directives(text) == (
        ('Directive1', 'value1'),
        '',
        ('Directive2', 'value2'),
    )


@pytest.mark.parametrize('line', (
    '# some comment line',
    '\t  # some comment line beginning with spaces',
    '  \t# some comment line beginning with spaces',
))
def test_comment_line(line):
    assert RobotsTxt.parse_directives(line) == ()


@pytest.mark.parametrize('line', (
    'Field: value # some inline comment',
    'Field: value \t # some inline comment',
    pytest.mark.xfail(reason='no space before # character')('Field: value# some inline comment'),
))
def test_inline_comment(line):
    assert RobotsTxt.parse_directives(line) == (('Field', 'value'), )
