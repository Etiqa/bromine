"""
Global Bromine exception and warning classes.
"""

from selenium.common.exceptions import (NoSuchElementException,
                                        StaleElementReferenceException)


class BromineException(Exception):
    """Base class for all Bromine custom exceptions."""


class NoSuchObjectError(BromineException):
    """Base error for queries returning no results"""


class NoSuchPageError(NoSuchObjectError):
    """Page is not registered with given application."""


class MultipleObjectsFoundError(BromineException):
    """Base error for queries returning multiple results, while only one was expected."""


class MultipleElementsFoundError(MultipleObjectsFoundError):
    """Multiple instances of a DOM element were found, but only one was expected."""
