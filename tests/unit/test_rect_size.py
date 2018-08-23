import pytest

from bromine.utils.geometry import RectSize


def test_adding_two_rect_sizes():
    assert RectSize(1, 2) + RectSize(3, 4) == RectSize(4, 6)


def test_subtracting_two_rect_sizes():
    assert RectSize(1, 2) - RectSize(1, 4) == RectSize(0, -2)


class TestRectSizeDecorator():

    def test_undecorated_value(self, undecorated_function):
        undecorated_value = undecorated_function()
        assert not isinstance(undecorated_value, RectSize)

    def test_decorated_value(self, decorated_function):
        decorated_value = decorated_function()
        assert isinstance(decorated_value, RectSize)

    def test_decorated_function(self, decorated_function, undecorated_function):
        assert decorated_function.__name__ == undecorated_function.__name__

    @pytest.fixture(name='undecorated_function')
    def undecorated_fixture(self):
        def some_function_returning_a_tuple():
            return (1, 2)

        return some_function_returning_a_tuple

    @pytest.fixture(name='decorated_function')
    def decorated_fixture(self, undecorated_function):
        return RectSize.wrapped(undecorated_function)
