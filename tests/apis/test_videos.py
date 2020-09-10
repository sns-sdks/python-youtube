import json
import unittest

import responses

import pyyoutube


class ApiVideoTest(unittest.TestCase):
    BASE_PATH = "testdata/apidata/videos/"
    BASE_URL = "https://www.googleapis.com/youtube/v3/videos"

    with open(BASE_PATH + "videos_info_single.json", "rb") as f:
        VIDEOS_INFO_SINGLE = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "videos_info_multi.json", "rb") as f:
        VIDEOS_INFO_MULTI = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "videos_chart_paged_1.json", "rb") as f:
        VIDEOS_CHART_PAGED_1 = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "videos_chart_paged_2.json", "rb") as f:
        VIDEOS_CHART_PAGED_2 = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "videos_myrating_paged_1.json", "rb") as f:
        VIDEOS_MYRATING_PAGED_1 = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "videos_myrating_paged_2.json", "rb") as f:
        VIDEOS_MYRATING_PAGED_2 = json.loads(f.read().decode("utf-8"))

    def setUp(self) -> None:
        self.api = pyyoutube.Api(api_key="api key")
        self.api_with_token = pyyoutube.Api(access_token="token")

    def testGetVideoById(self) -> None:
        with self.assertRaises(pyyoutube.PyYouTubeException):
            self.api.get_video_by_id(video_id="id", parts="id,not_part")

        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL, json=self.VIDEOS_INFO_SINGLE)
            m.add("GET", self.BASE_URL, json=self.VIDEOS_INFO_MULTI)

            res_by_single_id = self.api.get_video_by_id(
                video_id="D-lhorsDlUQ",
                parts="id,snippet,player",
                max_height=480,
                max_width=270,
                return_json=True,
            )
            self.assertEqual(res_by_single_id["kind"], "youtube#videoListResponse")
            self.assertEqual(res_by_single_id["pageInfo"]["totalResults"], 1)
            video = res_by_single_id["items"][0]
            self.assertEqual(video["id"], "D-lhorsDlUQ")
            self.assertEqual(
                video["player"]["embedHtml"],
                (
                    '\u003ciframe width="480" height="270" src="//www.youtube.com/embed/D-lhorsDlUQ" '
                    'frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; '
                    'picture-in-picture" allowfullscreen\u003e\u003c/iframe\u003e'
                ),
            )

            res_by_multi_id = self.api.get_video_by_id(
                video_id=["D-lhorsDlUQ", "ovdbrdCIP7U"]
            )
            self.assertEqual(res_by_multi_id.pageInfo.totalResults, 2)
            self.assertEqual(len(res_by_multi_id.items), 2)
            self.assertEqual(res_by_multi_id.items[0].id, "D-lhorsDlUQ")

    def testGetVideoByChart(self) -> None:
        with self.assertRaises(pyyoutube.PyYouTubeException):
            self.api.get_videos_by_chart(chart="mostPopular", parts="id,not_part")

        # test paged
        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL, json=self.VIDEOS_CHART_PAGED_1)
            m.add("GET", self.BASE_URL, json=self.VIDEOS_CHART_PAGED_2)

            res_by_chart = self.api.get_videos_by_chart(
                chart="mostPopular",
                region_code="US",
                category_id="0",
                max_height=480,
                max_width=270,
                count=20,
                limit=5,
                return_json=True,
            )
            self.assertEqual(res_by_chart["kind"], "youtube#videoListResponse")
            self.assertEqual(res_by_chart["pageInfo"]["totalResults"], 8)
            self.assertEqual(len(res_by_chart["items"]), 8)
            self.assertEqual(res_by_chart["items"][0]["id"], "hDeuSfo_Ys0")

        # test count
        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL, json=self.VIDEOS_CHART_PAGED_1)

            res_by_chart = self.api.get_videos_by_chart(chart="mostPopular", count=3)
            self.assertEqual(res_by_chart.pageInfo.totalResults, 8)
            self.assertEqual(len(res_by_chart.items), 3)
            self.assertEqual(res_by_chart.items[0].id, "hDeuSfo_Ys0")

        # test get all items
        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL, json=self.VIDEOS_CHART_PAGED_1)
            m.add("GET", self.BASE_URL, json=self.VIDEOS_CHART_PAGED_2)

            res_by_chart = self.api.get_videos_by_chart(chart="mostPopular", count=None)
            self.assertEqual(res_by_chart.pageInfo.totalResults, 8)

        # test use page token
        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL, json=self.VIDEOS_CHART_PAGED_2)

            res_by_chart = self.api.get_videos_by_chart(
                chart="mostPopular", count=None, page_token="CAUQAA"
            )
            self.assertEqual(len(res_by_chart.items), 3)

    def testGetVideoByMyRating(self) -> None:
        with self.assertRaises(pyyoutube.PyYouTubeException):
            self.api_with_token.get_videos_by_myrating(
                rating="like", parts="id,not_part"
            )

        # test need authorization
        with self.assertRaises(pyyoutube.PyYouTubeException):
            self.api.get_videos_by_myrating(rating="like", parts="id,not_part")

        # test paged
        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL, json=self.VIDEOS_MYRATING_PAGED_1)
            m.add("GET", self.BASE_URL, json=self.VIDEOS_MYRATING_PAGED_2)

            res_by_my_rating = self.api_with_token.get_videos_by_myrating(
                rating="like",
                parts=("id", "snippet", "player"),
                max_height=480,
                max_width=270,
                count=10,
                limit=2,
                return_json=True,
            )
            self.assertEqual(res_by_my_rating["kind"], "youtube#videoListResponse")
            self.assertEqual(res_by_my_rating["pageInfo"]["totalResults"], 3)
            self.assertEqual(len(res_by_my_rating["items"]), 3)
            self.assertEqual(res_by_my_rating["items"][0]["id"], "P4IfFLAX9hY")

        # test count
        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL, json=self.VIDEOS_MYRATING_PAGED_1)
            res_by_my_rating = self.api_with_token.get_videos_by_myrating(
                rating="like",
                parts=("id", "snippet", "player"),
                count=1,
                limit=2,
            )
            self.assertEqual(res_by_my_rating.pageInfo.totalResults, 3)
            self.assertEqual(len(res_by_my_rating.items), 1)
            self.assertEqual(res_by_my_rating.items[0].id, "P4IfFLAX9hY")

        # test get all items
        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL, json=self.VIDEOS_MYRATING_PAGED_1)
            m.add("GET", self.BASE_URL, json=self.VIDEOS_MYRATING_PAGED_2)
            res_by_my_rating = self.api_with_token.get_videos_by_myrating(
                rating="like",
                parts=("id", "snippet", "player"),
                count=None,
            )
            self.assertEqual(res_by_my_rating.pageInfo.totalResults, 3)

        # test use page token
        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL, json=self.VIDEOS_MYRATING_PAGED_2)

            res_by_my_rating = self.api_with_token.get_videos_by_myrating(
                rating="like",
                parts=("id", "snippet", "player"),
                count=None,
                page_token="CAIQAA",
            )
            self.assertEqual(len(res_by_my_rating.items), 1)
