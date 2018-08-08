"""
Global Bromine exception and warning classes.
"""

from selenium.common.exceptions import (NoSuchElementException,  # pylint: disable=unused-import
                                        StaleElementReferenceException)


class BromineException(Exception):
    """Base class for all Bromine custom exceptions."""


class MultipleObjectsFoundError(BromineException):
    """Base error for queries returning multiple results, while only one was expected."""


class MultipleElementsFoundError(MultipleObjectsFoundError):
    """Multiple instances of a DOM element were found, but only one was expected."""
