import unittest

import pyyoutube
from pyyoutube.utils.params_checker import enf_comma_separated, enf_parts


class ParamCheckerTest(unittest.TestCase):
    def testEnfCommaSeparated(self) -> None:
        self.assertIsNone(enf_comma_separated("id", None))
        self.assertEqual(enf_comma_separated("id", "my_id"), "my_id")
        self.assertEqual(enf_comma_separated("id", "id1,id2"), "id1,id2")
        self.assertEqual(enf_comma_separated("id", ["id1", "id2"]), "id1,id2")
        self.assertEqual(enf_comma_separated("id", ("id1", "id2")), "id1,id2")
        self.assertTrue(enf_comma_separated("id", {"id1", "id2"}))

        with self.assertRaises(pyyoutube.PyYouTubeException):
            enf_comma_separated("id", 1)
        with self.assertRaises(pyyoutube.PyYouTubeException):
            enf_comma_separated("id", [None, None])

    def testEnfParts(self) -> None:
        self.assertTrue(enf_parts(resource="channels", value=None))
        self.assertTrue(enf_parts(resource="channels", value="id"), "id")
        self.assertTrue(enf_parts(resource="channels", value="id,snippet"))
        self.assertTrue(enf_parts(resource="channels", value=["id", "snippet"]))
        self.assertTrue(enf_parts(resource="channels", value=("id", "snippet")))
        self.assertTrue(enf_parts(resource="channels", value={"id", "snippet"}))

        with self.assertRaises(pyyoutube.PyYouTubeException):
            enf_parts(resource="channels", value=1)

        with self.assertRaises(pyyoutube.PyYouTubeException):
            enf_parts(resource="channels", value="not_part")
