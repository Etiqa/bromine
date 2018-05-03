"""
A model of the World as a collection of browser sessions.

Ideally, this is the root of Bromine's conceptual model.

A session is a tuple that links a User, a WebDriver instance and an Application.
"""

from .exceptions import NoSuchObjectError, MultipleObjectsFoundError


class World(object):
    """A collection of Sessions."""

    def __init__(self):
        self._sessions = []

    def add_session(self, session):
        """Add a session to the World.

        Args:
            session: Session object to add

        Return:
            None
        """
        self._sessions.append(session)

    def remove_session(self, session):
        """Remove a session from the World.

        Args:
            session: Session object to remove

        Return:
            None
        """
        self._sessions.remove(session)

    def get_session(self, filter_func):
        """Find a session matching the criteria expressed by filter_func argument

        Args:
            filter_func: Function object used to filter this World's sessions.
                It takes a Session object as input parameter and has the same
                semantics as 'function' parameter of Python's built-in 'filter'

        Return:
            The Session object matching search criteria

        Raise:
            NoSuchObjectError if no session matches search criteria,
            MultipleObjectsFoundError if more than one session matches search criteria
        """
        search_results = list(self._get_sessions(filter_func))
        if not search_results:
            raise NoSuchObjectError
        elif len(search_results) > 1:
            raise MultipleObjectsFoundError
        return search_results[0]

    def _get_sessions(self, filter_func):
        return filter(filter_func, self._sessions)


class BrowserSession(object): # pylint: disable=too-few-public-methods
    """session = <browser, user, application>."""

    def __init__(self, browser, user, application):
        self.browser = browser
        self.user = user
        self.application = application


class User(object): # pylint: disable=too-few-public-methods
    """Basic user model."""

    def __init__(self, name):
        self._name = name

    @property
    def name(self): # pylint: disable=missing-docstring
        return self._name
