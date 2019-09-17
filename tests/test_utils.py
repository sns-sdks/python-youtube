import unittest

import pyyoutube
import pyyoutube.utils.params_checker as validator


class TestParamChecker(unittest.TestCase):
    def testCommaValidator(self):
        with self.assertRaises(pyyoutube.PyYouTubeException):
            validator.comma_separated_validator(kw1=1, kw2=2)
        validator.comma_separated_validator(kw1='1,2')

    def testPartsValidator(self):
        with self.assertRaises(pyyoutube.PyYouTubeException):
            validator.parts_validator('channels', 'id,part')
        validator.parts_validator('videos', 'id,snippet')

    def testIncompatibleValidator(self):
        with self.assertRaises(pyyoutube.PyYouTubeException):
            validator.incompatible_validator(kw1='1', kw2='2')
        with self.assertRaises(pyyoutube.PyYouTubeException):
            validator.incompatible_validator()

        validator.incompatible_validator(kw1='1')
        validator.incompatible_validator(kw1='1', kw2=None)
