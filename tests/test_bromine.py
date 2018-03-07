# pylint: disable=missing-docstring

import unittest
import bromine


class TestImport(unittest.TestCase):

    def test_import(self):
        self.assertTrue(bromine is not None)
