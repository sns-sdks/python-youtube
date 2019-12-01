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

    def setUp(self) -> None:
        self.api = pyyoutube.Api(api_key="api key")

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
