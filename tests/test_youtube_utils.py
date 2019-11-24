import unittest

from pyyoutube import youtube_utils as utils
from pyyoutube.error import PyYouTubeException


class UtilsTest(unittest.TestCase):
    def testDurationConvert(self):
        duration = "PT14H23M42S"
        self.assertEqual(utils.get_video_duration(duration), 51822)

        duration = "PT14H23M42"
        with self.assertRaises(PyYouTubeException):
            utils.get_video_duration(duration)
