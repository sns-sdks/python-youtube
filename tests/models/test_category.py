import json
import unittest

import pyyoutube.models as models


class CategoryModelTest(unittest.TestCase):
    BASE_PATH = "testdata/modeldata/categories/"

    with open(BASE_PATH + "video_category_info.json", "rb") as f:
        VIDEO_CATEGORY_INFO = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "video_category_response.json", "rb") as f:
        VIDEO_CATEGORY_RESPONSE = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "guide_category_info.json", "rb") as f:
        GUIDE_CATEGORY_INFO = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "guide_category_response.json", "rb") as f:
        GUIDE_CATEGORY_RESPONSE = json.loads(f.read().decode("utf-8"))

    def testVideoCategory(self) -> None:
        m = models.VideoCategory.from_dict(self.VIDEO_CATEGORY_INFO)
        self.assertEqual(m.id, "17")
        self.assertEqual(m.snippet.title, "Sports")

    def testVideoCategoryListResponse(self) -> None:
        m = models.VideoCategoryListResponse.from_dict(self.VIDEO_CATEGORY_RESPONSE)
        self.assertEqual(m.kind, "youtube#videoCategoryListResponse")
        self.assertEqual(len(m.items), 1)
        self.assertEqual(m.items[0].id, "17")
