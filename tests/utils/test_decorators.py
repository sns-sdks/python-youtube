import unittest

import pyyoutube
from pyyoutube.utils.constants import CHANNEL_RESOURCE_PROPERTIES
from pyyoutube.utils.decorators import comma_separated, incompatible, parts_validator


class DecoratorTest(unittest.TestCase):
    def testIncompatibleDecorator(self) -> None:
        @incompatible(params=["p1", "p2"])
        def function(*, p1=None, p2=None, p3=3):
            if p1 is None:
                return p2 + p3
            if p2 is None:
                return p1 + p3

        self.assertEqual(function(p1=1), 4)
        self.assertEqual(function(p2=1), 4)

        with self.assertRaises(pyyoutube.PyYouTubeException):
            function()
        with self.assertRaises(pyyoutube.PyYouTubeException):
            function(p1=1, p2=2)

    def testPartsValidator(self) -> None:
        @parts_validator(resource="channels")
        def function(*, parts=None):
            return parts

        self.assertEqual(function(), CHANNEL_RESOURCE_PROPERTIES)
        self.assertEqual(function(parts="id,snippet"), {"id", "snippet"})
        self.assertEqual(function(parts=["id", "snippet"]), {"id", "snippet"})
        self.assertEqual(function(parts=("id", "snippet")), {"id", "snippet"})
        self.assertEqual(function(parts={"id", "snippet"}), {"id", "snippet"})

        with self.assertRaises(pyyoutube.PyYouTubeException):
            function(parts={"p": "art"})
        with self.assertRaises(pyyoutube.PyYouTubeException):
            function(parts="not_part")

    def testCommaSeparated(self) -> None:
        @comma_separated(params=["c_id"])
        def function(*, c_id=None):
            return c_id

        self.assertEqual(function(), None)
        self.assertEqual(function(c_id="id1,id2"), "id1,id2")
        self.assertEqual(function(c_id=["id1", "id2"]), "id1,id2")
        self.assertEqual(function(c_id=("id1", "id2")), "id1,id2")

        with self.assertRaises(pyyoutube.PyYouTubeException):
            function(c_id=1)
