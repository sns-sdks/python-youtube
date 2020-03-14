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

    def testSearchByLocation(self) -> None:
        with open(self.BASE_PATH + "search_by_location.json", "rb") as f:
            search_by_location = json.loads(f.read().decode("utf-8"))

        with self.assertRaises(pyyoutube.PyYouTubeException):
            self.api.search_by_location(location=(12, 12), location_radius="")

        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL, json=search_by_location)
            res = self.api.search_by_location(
                location=(21.5922529, -158.1147114),
                location_radius="10mi",
                keywords="surfing",
                parts=["snippet"],
                count=5,
            )
            self.assertEqual(res.pageInfo.resultsPerPage, 5)
            self.assertEqual(len(res.items), 5)
            self.assertEqual(res.items[0].snippet.channelId, "UCOtHosOqPe9d6vLy-8LfHzQ")

    def testSearchByEvent(self) -> None:
        with open(self.BASE_PATH + "search_by_event.json", "rb") as f:
            search_by_event = json.loads(f.read().decode("utf-8"))

        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL, json=search_by_event)
            res = self.api.search_by_event(
                event_type="live", keywords="news", parts=["snippet"], count=5
            )

            self.assertEqual(res.pageInfo.resultsPerPage, 5)
            self.assertEqual(len(res.items), 5)
            self.assertEqual(res.items[0].snippet.channelId, "UCZMsvbAhhRblVGXmEXW8TSA")

    def testSearchByRelatedToVideoId(self) -> None:
        with open(self.BASE_PATH + "search_by_related_video.json", "rb") as f:
            search_by_related_video = json.loads(f.read().decode("utf-8"))

        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL, json=search_by_related_video)

            res = self.api.search_by_related_video(
                related_to_video_id="Ks-_Mh1QhMc",
                region_code="US",
                relevance_language="en",
                safe_search="moderate",
                count=5,
            )

            self.assertEqual(res.pageInfo.resultsPerPage, 5)
            self.assertEqual(len(res.items), 5)
            self.assertEqual(res.regionCode, "US")
            self.assertEqual(res.items[0].snippet.channelId, "UCAuUUnT6oDeKwE6v1NGQxug")

    def testSearch(self) -> None:
        with open(self.BASE_PATH + "search_by_dev.json", "rb") as f:
            search_by_dev = json.loads(f.read().decode("utf-8"))

        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL, json=search_by_dev)

            res_dev = self.api.search(parts=["snippet"], for_developer=True, count=5)

            self.assertEqual(res_dev.pageInfo.resultsPerPage, 5)
            self.assertEqual(
                res_dev.items[0].snippet.channelId, "UCstEtN0pgOmCf02EdXsGChw"
            )
