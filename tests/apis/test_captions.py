import json
import unittest

import responses

import pyyoutube


class ApiCaptionsTest(unittest.TestCase):
    BASE_PATH = "testdata/apidata/captions/"
    BASE_URL = "https://www.googleapis.com/youtube/v3/captions"

    with open(BASE_PATH + "captions_by_video.json", "rb") as f:
        CAPTIONS_BY_VIDEO = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "captions_filter_by_id.json", "rb") as f:
        CAPTIONS_FILTER_ID = json.loads(f.read().decode("utf-8"))

    def setUp(self) -> None:
        self.api_with_access_token = pyyoutube.Api(access_token="token")

    def testGetCaptionByVideo(self) -> None:
        video_id = "oHR3wURdJ94"

        # test parts
        with self.assertRaises(pyyoutube.PyYouTubeException):
            self.api_with_access_token.get_captions_by_video(
                video_id=video_id,
                parts="id,not_part",
            )

        # test by video
        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL, json=self.CAPTIONS_BY_VIDEO)

            res = self.api_with_access_token.get_captions_by_video(
                video_id=video_id,
                parts="id,snippet",
                return_json=True,
            )
            self.assertEqual(len(res["items"]), 2)
            self.assertEqual(res["items"][0]["snippet"]["videoId"], video_id)

        # test filter id
        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL, json=self.CAPTIONS_FILTER_ID)

            res = self.api_with_access_token.get_captions_by_video(
                video_id=video_id,
                parts=["id", "snippet"],
                caption_id="SwPOvp0r7kd9ttt_XhcHdZthMwXG7Z0I",
            )

            self.assertEqual(len(res.items), 1)
            self.assertEqual(res.items[0].snippet.videoId, video_id)
