import json
import unittest

import responses

import pyyoutube


class ApiVideoCategoryTest(unittest.TestCase):
    BASE_PATH = "testdata/apidata/categories/"
    BASE_URL = "https://www.googleapis.com/youtube/v3/videoCategories"

    with open(BASE_PATH + "video_category_single.json", "rb") as f:
        VIDEO_CATEGORY_SINGLE = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "video_category_multi.json", "rb") as f:
        VIDEO_CATEGORY_MULTI = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "video_category_by_region.json", "rb") as f:
        VIDEO_CATEGORY_BY_REGION = json.loads(f.read().decode("utf-8"))

    def setUp(self) -> None:
        self.api = pyyoutube.Api(api_key="api key")

    def testGetVideoCategories(self) -> None:
        # test params
        with self.assertRaises(pyyoutube.PyYouTubeException):
            self.api.get_video_categories()
        # test parts
        with self.assertRaises(pyyoutube.PyYouTubeException):
            self.api.get_video_categories(category_id="id", parts="id,not_part")

        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL, json=self.VIDEO_CATEGORY_SINGLE)
            m.add("GET", self.BASE_URL, json=self.VIDEO_CATEGORY_MULTI)
            m.add("GET", self.BASE_URL, json=self.VIDEO_CATEGORY_BY_REGION)

            res_by_single = self.api.get_video_categories(
                category_id="17",
                parts=["id", "snippet"],
                return_json=True,
            )
            self.assertEqual(res_by_single["kind"], "youtube#videoCategoryListResponse")
            self.assertEqual(len(res_by_single["items"]), 1)
            self.assertEqual(res_by_single["items"][0]["id"], "17")

            res_by_multi = self.api.get_video_categories(
                category_id=["17", "18"],
                parts="id,snippet",
            )
            self.assertEqual(len(res_by_multi.items), 2)
            self.assertEqual(res_by_multi.items[1].id, "18")

            res_by_region = self.api.get_video_categories(
                region_code="US",
                parts="id,snippet",
            )
            self.assertEqual(len(res_by_region.items), 32)
            self.assertEqual(res_by_region.items[0].id, "1")
