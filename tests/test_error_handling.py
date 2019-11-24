import unittest

import responses

import pyyoutube


class ErrorTest(unittest.TestCase):
    BASE_URL = "https://www.googleapis.com/youtube/v3/"

    def setUp(self) -> None:
        self.base_path = "testdata/"
        self.api = pyyoutube.Api(api_key="test")

    @responses.activate
    def testResponseError(self):
        with open(f"{self.base_path}error_response.json") as f:
            res_data = f.read()
        responses.add(
            responses.GET, self.BASE_URL + "channels", body=res_data, status=400
        )
        with self.assertRaises(pyyoutube.PyYouTubeException) as e:
            self.api.get_channel_info(channel_id="UC_x5XG1OV2P6uZZ5FSM9Ttw")
            self.assertEqual(e.status_code, 400)
            self.assertEqual(
                repr(e), "PyYouTubeException(status_code=400, message=Bad Request)"
            )

    def testErrorMessage(self):
        with self.assertRaises(pyyoutube.PyYouTubeException) as e:
            self.api.get_channel_info(channel_id=None)
            self.assertEqual(e.status_code, 10005)
