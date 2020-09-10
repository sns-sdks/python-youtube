import json
import unittest

import responses
import pyyoutube


class ApiCommentThreadTest(unittest.TestCase):
    BASE_PATH = "testdata/apidata/comment_threads/"
    BASE_URL = "https://www.googleapis.com/youtube/v3/commentThreads"

    with open(BASE_PATH + "comment_thread_single.json", "rb") as f:
        COMMENT_THREAD_INFO_SINGLE = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "comment_threads_multi.json", "rb") as f:
        COMMENT_THREAD_INFO_MULTI = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "comment_threads_all_to_me.json", "rb") as f:
        COMMENT_THREAD_ALL_TO_ME = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "comment_threads_by_channel.json", "rb") as f:
        COMMENT_THREAD_BY_CHANNEL = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "comment_threads_with_search.json", "rb") as f:
        COMMENT_THREAD_BY_SEARCH = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "comment_threads_by_video_paged_1.json", "rb") as f:
        COMMENT_THREAD_BY_VIDEO_P_1 = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "comment_threads_by_video_paged_2.json", "rb") as f:
        COMMENT_THREAD_BY_VIDEO_P_2 = json.loads(f.read().decode("utf-8"))

    def setUp(self) -> None:
        self.api = pyyoutube.Api(api_key="api key")
        self.api_with_token = pyyoutube.Api(access_token="access token")

    def testGetCommentThreadById(self) -> None:
        # test parts
        with self.assertRaises(pyyoutube.PyYouTubeException):
            self.api.get_comment_thread_by_id(
                comment_thread_id="id", parts="id,not_part"
            )

        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL, json=self.COMMENT_THREAD_INFO_SINGLE)
            m.add("GET", self.BASE_URL, json=self.COMMENT_THREAD_INFO_MULTI)

            res_by_single_id = self.api.get_comment_thread_by_id(
                comment_thread_id="UgxKREWxIgDrw8w2e_Z4AaABAg",
                parts="id,snippet",
                text_format="plain_text",
                return_json=True,
            )
            self.assertEqual(
                res_by_single_id["kind"], "youtube#commentThreadListResponse"
            )
            self.assertEqual(len(res_by_single_id["items"]), 1)
            self.assertEqual(
                res_by_single_id["items"][0]["id"], "UgxKREWxIgDrw8w2e_Z4AaABAg"
            )

            res_by_multi_id = self.api.get_comment_thread_by_id(
                comment_thread_id=[
                    "UgxKREWxIgDrw8w2e_Z4AaABAg",
                    "UgyrVQaFfEdvaSzstj14AaABAg",
                ],
                parts=["id", "snippet"],
            )
            self.assertEqual(res_by_multi_id.pageInfo.totalResults, 2)
            self.assertEqual(res_by_multi_id.items[1].id, "UgyrVQaFfEdvaSzstj14AaABAg")

    def testGetCommentThreads(self) -> None:
        # test no params
        with self.assertRaises(pyyoutube.PyYouTubeException):
            self.api.get_comment_threads()
        # test parts
        with self.assertRaises(pyyoutube.PyYouTubeException):
            self.api.get_comment_threads(all_to_channel_id="id", parts="id,not_part")

        # test with all to channel.
        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL, json=self.COMMENT_THREAD_ALL_TO_ME)

            res_by_all = self.api_with_token.get_comment_threads(
                all_to_channel_id="UCa-vrCLQHviTOVnEKDOdetQ",
                parts="id,snippet",
                moderation_status="published",
                order="time",
                return_json=True,
            )
            self.assertEqual(res_by_all["kind"], "youtube#commentThreadListResponse")
            self.assertEqual(res_by_all["pageInfo"]["totalResults"], 4)
            self.assertEqual(len(res_by_all["items"]), 4)
            self.assertEqual(res_by_all["items"][0]["id"], "UgyWeTdgc4sc1xgmbld4AaABAg")

        # test with channel
        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL, json=self.COMMENT_THREAD_BY_CHANNEL)

            res_by_channel = self.api.get_comment_threads(
                channel_id="UC_x5XG1OV2P6uZZ5FSM9Ttw",
            )
            self.assertEqual(res_by_channel.pageInfo.totalResults, 2)
            self.assertEqual(
                res_by_channel.items[0].snippet.channelId, "UC_x5XG1OV2P6uZZ5FSM9Ttw"
            )

        # test with search
        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL, json=self.COMMENT_THREAD_BY_SEARCH)

            res_by_search = self.api.get_comment_threads(
                channel_id="UC_x5XG1OV2P6uZZ5FSM9Ttw",
                search_terms="Hello",
            )
            self.assertEqual(res_by_search.pageInfo.totalResults, 1)
            self.assertEqual(
                res_by_channel.items[0].snippet.channelId, "UC_x5XG1OV2P6uZZ5FSM9Ttw"
            )
            self.assertIn(
                "Hello",
                res_by_channel.items[0].snippet.topLevelComment.snippet.textDisplay,
            )

        # test with video
        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL, json=self.COMMENT_THREAD_BY_VIDEO_P_1)
            m.add("GET", self.BASE_URL, json=self.COMMENT_THREAD_BY_VIDEO_P_2)

            res_by_video = self.api.get_comment_threads(
                video_id="F1UP7wRCPH8",
                count=8,
                limit=5,
            )
            self.assertEqual(len(res_by_video.items), 8)
            self.assertEqual(res_by_video.items[0].snippet.videoId, "F1UP7wRCPH8")

        # test get all items
        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL, json=self.COMMENT_THREAD_BY_VIDEO_P_1)
            m.add("GET", self.BASE_URL, json=self.COMMENT_THREAD_BY_VIDEO_P_2)

            res_by_video = self.api.get_comment_threads(
                video_id="F1UP7wRCPH8",
                count=None,
            )
            self.assertEqual(len(res_by_video.items), 10)

        # test use page token
        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL, json=self.COMMENT_THREAD_BY_VIDEO_P_2)

            res_by_video = self.api.get_comment_threads(
                video_id="F1UP7wRCPH8",
                count=None,
                page_token="QURTSl9pMzdZOUVzMkI0czlmRmNjSVBPcTBTdzVzajUydDVnbE5SNElWS0l5WU12amYweVotdzF5c1hTNmxzUmVIcEZXbmVEVFMzNVJmWk82TVVwUlB2LWh5aUpOQlA5TGQzTWZEcHlTeTd2dlNGRUFZaVF0cmtJd01BTHlnOG0=",
            )
            self.assertEqual(len(res_by_video.items), 5)
