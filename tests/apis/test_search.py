import json
import unittest

import responses

import pyyoutube


class ApiSearchTest(unittest.TestCase):
    BASE_PATH = "testdata/apidata/search/"
    BASE_URL = "https://www.googleapis.com/youtube/v3/search"

    def setUp(self) -> None:
        self.api = pyyoutube.Api(api_key="api key")

    def testSearchByKeywords(self) -> None:
        with open(self.BASE_PATH + "search_by_keywords_p1.json", "rb") as f:
            res_p1 = json.loads(f.read().decode("utf-8"))
        with open(self.BASE_PATH + "search_by_keywords_p2.json", "rb") as f:
            res_p2 = json.loads(f.read().decode("utf-8"))

        # test parts
        with self.assertRaises(pyyoutube.PyYouTubeException):
            self.api.search_by_keywords(keywords="x", parts="id,not_part")

        # test response
        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL, json=res_p1)
            m.add("GET", self.BASE_URL, json=res_p2)

            res_json = self.api.search_by_keywords(
                keywords="surfing", count=30, limit=25, return_json=True
            )
            self.assertEqual(res_json["kind"], "youtube#searchListResponse")
            self.assertEqual(res_json["regionCode"], "JP")
            self.assertEqual(res_json["pageInfo"]["totalResults"], 1000000)
            self.assertEqual(len(res_json["items"]), 30)

            res = self.api.search_by_keywords(
                keywords="surfing", parts=["id", "snippet"], count=25,
            )
            self.assertEqual(res.pageInfo.resultsPerPage, 25)
            self.assertEqual(res.items[0].id.videoId, "-2IlD-x8wvY")
            self.assertEqual(res.items[0].snippet.channelId, "UCeYue9Nbodzg3T1Nt88E3fg")
