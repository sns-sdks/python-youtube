import json
import unittest

import responses

import pyyoutube


class ApiSearchTest(unittest.TestCase):
    BASE_PATH = "testdata/apidata/search/"
    BASE_URL = "https://www.googleapis.com/youtube/v3/search"

    def setUp(self) -> None:
        self.api = pyyoutube.Api(api_key="api key")

    def testSearch(self) -> None:
        with open(self.BASE_PATH + "search_videos_by_channel.json", "rb") as f:
            search_videos_by_channel = json.loads(f.read().decode("utf-8"))
        with open(self.BASE_PATH + "search_by_location.json", "rb") as f:
            search_by_location = json.loads(f.read().decode("utf-8"))
        with open(self.BASE_PATH + "search_by_event.json", "rb") as f:
            search_by_event = json.loads(f.read().decode("utf-8"))
        with open(self.BASE_PATH + "search_channels.json", "rb") as f:
            search_channels = json.loads(f.read().decode("utf-8"))

        # test search videos with channel
        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL, json=search_videos_by_channel)

            res = self.api.search(
                parts="snippet",
                channel_id="UC_x5XG1OV2P6uZZ5FSM9Ttw",
                q="news",
                count=5,
            )
            self.assertEqual(res.items[0].id.videoId, "LrQWzOkC0XQ")
            self.assertEqual(res.items[0].snippet.channelId, "UC_x5XG1OV2P6uZZ5FSM9Ttw")

        # test search locations
        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL, json=search_by_location)
            res = self.api.search(
                location="21.5922529, -158.1147114",
                location_radius="10mi",
                q="surfing",
                parts=["snippet"],
                count=5,
                published_after="2020-02-01T00:00:00Z",
                published_before="2020-03-01T00:00:00Z",
                safe_search="moderate",
                search_type="video",
            )
            self.assertEqual(res.pageInfo.resultsPerPage, 5)
            self.assertEqual(len(res.items), 5)
            self.assertEqual(res.items[0].snippet.channelId, "UCo_q6aOlvPH7M-j_XGWVgXg")

        # test search event
        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL, json=search_by_event)
            res = self.api.search(
                event_type="live",
                q="news",
                count=25,
                limit=25,
                parts=["snippet"],
                search_type="video",
                topic_id="/m/09s1f",
                order="viewCount",
            )

            self.assertEqual(res.pageInfo.resultsPerPage, 25)
            self.assertEqual(len(res.items), 25)
            self.assertEqual(res.items[0].snippet.channelId, "UCDGiCfCZIV5phsoGiPwIcyQ")

        # test search channel
        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL, json=search_channels)

            res_channels = self.api.search(
                parts=["snippet"],
                channel_type="any",
                count=5,
                search_type="channel",
            )
            self.assertEqual(res_channels.pageInfo.resultsPerPage, 5)
            self.assertEqual(
                res_channels.items[0].snippet.channelId, "UCxRULEz6kS0PMxCzOY25GhQ"
            )

    def testSearchByKeywords(self) -> None:
        with open(self.BASE_PATH + "search_by_keywords_p1.json", "rb") as f:
            res_p1 = json.loads(f.read().decode("utf-8"))
        with open(self.BASE_PATH + "search_by_keywords_p2.json", "rb") as f:
            res_p2 = json.loads(f.read().decode("utf-8"))

        # test parts
        with self.assertRaises(pyyoutube.PyYouTubeException):
            self.api.search_by_keywords(q="x", parts="id,not_part")

        # test response
        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL, json=res_p1)
            m.add("GET", self.BASE_URL, json=res_p2)

            res_json = self.api.search_by_keywords(
                q="surfing", count=30, limit=25, return_json=True
            )
            self.assertEqual(res_json["kind"], "youtube#searchListResponse")
            self.assertEqual(res_json["regionCode"], "JP")
            self.assertEqual(res_json["pageInfo"]["totalResults"], 1000000)
            self.assertEqual(len(res_json["items"]), 30)

            res = self.api.search_by_keywords(
                q="surfing",
                parts=["id", "snippet"],
                count=25,
            )
            self.assertEqual(res.pageInfo.resultsPerPage, 25)
            self.assertEqual(res.items[0].id.videoId, "-2IlD-x8wvY")
            self.assertEqual(res.items[0].snippet.channelId, "UCeYue9Nbodzg3T1Nt88E3fg")

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

    def testSearchByDeveloper(self) -> None:
        with open(self.BASE_PATH + "search_by_developer.json", "rb") as f:
            search_by_developer = json.loads(f.read().decode("utf-8"))

        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL, json=search_by_developer)

            res_dev = self.api.search_by_developer(
                parts=["snippet"],
                q="news",
                count=5,
                page_token="CAUQAA",
                video_category_id="17",
                video_caption="any",
                video_definition="any",
                video_dimension="any",
                video_duration="any",
                video_embeddable="any",
                video_license="any",
                video_syndicated="any",
                video_type="any",
            )
            self.assertEqual(res_dev.pageInfo.resultsPerPage, 5)
            self.assertEqual(
                res_dev.items[0].snippet.channelId, "UCeY0bbntWzzVIaj2z3QigXg"
            )

    def testSearchByMine(self) -> None:
        with open(self.BASE_PATH + "search_by_mine.json", "rb") as f:
            search_by_mine = json.loads(f.read().decode("utf-8"))

        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL, json=search_by_mine)

            res_mine = self.api.search_by_mine(
                parts=["snippet"],
            )

            self.assertEqual(res_mine.pageInfo.totalResults, 2)
            self.assertEqual(
                res_mine.items[0].snippet.channelId, "UCa-vrCLQHviTOVnEKDOdetQ"
            )
