from collections import namedtuple
from functools import wraps


class Point(namedtuple('Point', ('x', 'y'))):

    def __add__(self, other):
        return self.__class__(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return self.__add__(-other)

    def __neg__(self):
        return self.__class__(-self.x, -self.y)


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

    def as_PIL_box(self):
        return (self.x, self.y, self.x + self.width, self.y + self.height)
