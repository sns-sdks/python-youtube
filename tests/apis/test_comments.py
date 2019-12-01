import json
import unittest

import responses

import pyyoutube


class ApiCommentTest(unittest.TestCase):
    BASE_PATH = "testdata/apidata/comments/"
    BASE_URL = "https://www.googleapis.com/youtube/v3/comments"

    with open(BASE_PATH + "comments_single.json", "rb") as f:
        COMMENTS_INFO_SINGLE = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "comments_multi.json", "rb") as f:
        COMMENTS_INFO_MULTI = json.loads(f.read().decode("utf-8"))

    def setUp(self) -> None:
        self.api = pyyoutube.Api(api_key="api key")

    def testGetCommentById(self) -> None:
        # test parts
        with self.assertRaises(pyyoutube.PyYouTubeException):
            self.api.get_comment_by_id(comment_id="id", parts="id,not_part")

        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL, json=self.COMMENTS_INFO_SINGLE)
            m.add("GET", self.BASE_URL, json=self.COMMENTS_INFO_MULTI)

            res_by_single = self.api.get_comment_by_id(
                comment_id="UgyUBI0HsgL9emxcZpR4AaABAg",
                parts=["id", "snippet"],
                return_json=True,
            )
            self.assertEqual(res_by_single["kind"], "youtube#commentListResponse")
            self.assertEqual(len(res_by_single["items"]), 1)
            self.assertEqual(
                res_by_single["items"][0]["id"], "UgyUBI0HsgL9emxcZpR4AaABAg"
            )

            res_by_multi = self.api.get_comment_by_id(
                comment_id=["UgyUBI0HsgL9emxcZpR4AaABAg", "Ugzi3lkqDPfIOirGFLh4AaABAg"],
                parts=("id", "snippet"),
            )
            self.assertEqual(len(res_by_multi.items), 2)
            self.assertEqual(res_by_multi.items[1].id, "Ugzi3lkqDPfIOirGFLh4AaABAg")
