"""
Global Bromine exception and warning classes.
"""


class BromineException(Exception):
    """Base class for all Bromine custom exceptions"""


class NoSuchPageError(BromineException):
    """Page is not registered with given application"""
