from collections import namedtuple
from functools import wraps


class Point(namedtuple('Point', ('x', 'y'))):

    def __add__(self, other):
        return self.__class__(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return self.__add__(-other)

    def __neg__(self):
        return self.__class__(-self.x, -self.y)

    def __rmul__(self, scalar_value):
        return self.__class__(scalar_value * self.x, scalar_value * self.y)


class RectSize(namedtuple('RectSize', ('width', 'height')), Point):
    """RectSize is just a Point with 'x', 'y' renamed to 'width', 'height'.

    >>> r = RectSize(1, 2)
    >>> r.width
    1
    >>> r.height
    2
    >>> r.x == r.width
    True
    >>> r.y == r.height
    True

    But:
    >>> RecSize(x=1, y=2)
    TypeError: __new__() got an unexpected keyword argument 'x'
    """

    @classmethod
    def wrapped(cls, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            value = func(*args, **kwargs)
            return cls(*value)
        return wrapper


class Rectangle(namedtuple('Rectangle', ('x', 'y', 'width', 'height'))):

    @property
    def upper_left_corner(self):
        return Point(self.x, self.y)

    @property
    def size(self):
        return RectSize(self.width, self.height)

    @property
    def left(self):
        return self.x

    @property
    def top(self):
        return self.y

    @property
    def right(self):
        return self.left + self.width -1

    @property
    def bottom(self):
        return self.top + self.height -1

    @classmethod
    def from_corner_and_size(cls, upper_left_corner, size):
        x, y = upper_left_corner
        width, height = size
        return cls(x, y, width, height)


def PIL_box(rectangle):
    """Represent a Rectangle in PIL's Coordinate System.

    See https://pillow.readthedocs.io/en/stable/handbook/concepts.html#coordinate-system
    """
    x, y, width, height = rectangle
    return (x, y, x + width, y + height)
