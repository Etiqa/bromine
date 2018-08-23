import pytest


class _BaseWindowTest(object):

    def test_outer_size(self):
        raise NotImplementedError

    def test_inner_size(self):
        raise NotImplementedError

    def test_virtual_pixel_ratio(self):
        raise NotImplementedError

    def test_physical_pixel_ratio(self):
        raise NotImplementedError

    def test_screenshot(self):
        raise NotImplementedError


@pytest.mark.skip(reason="TODO: this test has not been implemented yet") # TODO: write test
class TestWindow(_BaseWindowTest):

    def test_outer_size_is_readonly(self):
        raise NotImplementedError

    def test_inner_size_is_readonly(self):
        raise NotImplementedError


@pytest.mark.skip(reason="TODO: this test has not been implemented yet") # TODO: write test
class TestResizableWindow(_BaseWindowTest):

    def test_outer_size_can_be_modified(self):
        raise NotImplementedError

    def test_inner_size_can_be_modified(self):
        raise NotImplementedError

    def test_maximize(self):
        raise NotImplementedError
