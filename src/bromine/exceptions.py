"""
Global Bromine exception and warning classes.
"""

import selenium.common.exceptions as _se


class BromineException(Exception):
    """Base class for all Bromine custom exceptions."""


class NoSuchObjectError(BromineException):
    """Base error for queries returning no results"""


class NoSuchPageError(NoSuchObjectError):
    """Page is not registered with given application."""


class NoSuchElementException(_se.NoSuchElementException, NoSuchObjectError):
    """Wrapper of Selenium's NoSuchElementException."""


class MultipleObjectsFoundError(BromineException):
    """Base error for queries returning multiple results, while only one was expected."""


class MultipleElementsFoundError(MultipleObjectsFoundError):
    """Multiple instances of a DOM element were found, but only one was expected."""


class StaleElementReferenceException(_se.StaleElementReferenceException, BromineException):
    """Wrapper of Selenium's StaleElementReferenceException."""
