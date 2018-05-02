import pytest

from bromine import World, BrowserSession, User
from bromine.exceptions import NoSuchObjectError, MultipleObjectsFoundError


def test_new_session():
    user = User('some user')
    browser = None
    application = None
    session = BrowserSession(browser, user, application)
    world = World()
    world.add_session(session)


def test_get_session():
    world = World()
    world.add_session(BrowserSession(None, User('user_1'), None))
    session_1 = world.get_session(lambda s: s.user.name == 'user_1')
    assert session_1.user.name == 'user_1'


def test_session_not_found_error():
    world = World()
    world.add_session(BrowserSession(None, User('user_1'), None))
    with pytest.raises(NoSuchObjectError):
        world.get_session(lambda s: s.user.name == 'user_2')


def test_multiple_sessions_found_error(): # pylint: disable=invalid-name
    world = World()
    world.add_session(BrowserSession(None, User('user_1'), None))
    world.add_session(BrowserSession(None, User('user_1'), None))
    with pytest.raises(MultipleObjectsFoundError):
        world.get_session(lambda s: s.user.name == 'user_1')


def test_remove_session():
    world = World()
    world.add_session(BrowserSession(None, User('user_1'), None))
    world.add_session(BrowserSession(None, User('user_2'), None))
    session_1 = world.get_session(lambda s: s.user.name == 'user_1')
    world.remove_session(session_1)
    with pytest.raises(NoSuchObjectError):
        world.get_session(lambda s: s is session_1)
