import json
import unittest

import pyyoutube.models as models


class CategoryModelTest(unittest.TestCase):
    BASE_PATH = "testdata/modeldata/categories/"

    with open(BASE_PATH + "video_category_info.json", "rb") as f:
        VIDEO_CATEGORY_INFO = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "guide_category_info.json", "rb") as f:
        GUIDE_CATEGORY_INFO = json.loads(f.read().decode("utf-8"))

    def testVideoCategory(self) -> None:
        m = models.GuideCategory.from_dict(self.VIDEO_CATEGORY_INFO)

        self.assertEqual(m.id, "17")
        self.assertEqual(m.snippet.title, "Sports")

    def testGuideCategory(self) -> None:
        m = models.GuideCategory.from_dict(self.GUIDE_CATEGORY_INFO)

        self.assertEqual(m.id, "GCQmVzdCBvZiBZb3VUdWJl")
        self.assertEqual(m.snippet.title, "Best of YouTube")
