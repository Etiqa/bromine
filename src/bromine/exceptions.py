"""
Global Bromine exception and warning classes.
"""

import selenium.common.exceptions as _se


class BromineException(Exception):
    """Base class for all Bromine custom exceptions."""


class NoSuchPageError(BromineException):
    """Page is not registered with given application."""


class NoSuchElementException(_se.NoSuchElementException, BromineException):
    """Wrapper of Selenium's NoSuchElementException."""


class MultipleElementsFoundError(BromineException):
    """Multiple instances of a DOM element were found, but only one was expected."""


class StaleElementReferenceException(_se.StaleElementReferenceException, BromineException):
    """Wrapper of Selenium's StaleElementReferenceException."""
