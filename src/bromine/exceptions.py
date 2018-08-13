"""
Global Bromine exception and warning classes.
"""

from selenium.common.exceptions import (NoSuchElementException,  # pylint: disable=unused-import
                                        StaleElementReferenceException,
                                        TimeoutException)


class BromineException(Exception):
    """Base class for all Bromine custom exceptions."""


class MultipleElementsFoundError(BromineException):
    """Multiple instances of a DOM element were found, but only one was expected."""
