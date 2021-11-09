import json
import unittest

from requests import HTTPError

import pyyoutube
import responses


class ApiChannelTest(unittest.IsolatedAsyncioTestCase):
    BASE_PATH = "testdata/apidata/"
    BASE_URL = "https://www.googleapis.com/youtube/v3/channels"

    with open(BASE_PATH + "channel_info_single.json", "rb") as f:
        CHANNELS_INFO_SINGLE = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "channel_info_multi.json", "rb") as f:
        CHANNELS_INFO_MULTI = json.loads(f.read().decode("utf-8"))

    def setUp(self) -> None:
        self.api = pyyoutube.Api(self.session, api_key="api key")

    async def testSendRequest(self) -> None:
        with self.assertRaises(pyyoutube.PyYouTubeException):
            api = pyyoutube.Api(client_id="id", client_secret="secret")
            await api._request("channels", post_args={"a": "a"})
        with responses.RequestsMock() as m:
            m.add("POST", self.BASE_URL, json={})
            api = pyyoutube.Api(access_token="access token")
            res = await api._request("channels", post_args={"a": "a"})
            self.assertTrue(res)

        with self.assertRaises(pyyoutube.PyYouTubeException):
            with responses.RequestsMock() as m:
                m.add("GET", self.BASE_URL, body=HTTPError("Exception"))
                await self.api.get_channel_info(channel_id="channel_id", parts="id,snippet")

    # TODO need to separate.
    async def testParseResponse(self) -> None:
        with open("testdata/error_response.json", "rb") as f:
            error_response = json.loads(f.read().decode("utf-8"))

        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL, json=error_response, status=400)

            with self.assertRaises(pyyoutube.PyYouTubeException):
                await self.api.get_channel_info(
                    channel_id="UC_x5XG1OV2P6uZZ5FSM9Ttw", parts="id,snippet,statistics"
                )

    async def testGetChannelInfo(self) -> None:
        # test params checker
        with self.assertRaises(pyyoutube.PyYouTubeException):
            await self.api.get_channel_info(parts="id,invideoPromotion")
        with self.assertRaises(pyyoutube.PyYouTubeException):
            await self.api.get_channel_info()

        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL, json=self.CHANNELS_INFO_SINGLE)

            res_by_channel_id = await self.api.get_channel_info(
                channel_id="UC_x5XG1OV2P6uZZ5FSM9Ttw", parts="id,snippet,statistics"
            )
            self.assertEqual(res_by_channel_id.items[0].id, "UC_x5XG1OV2P6uZZ5FSM9Ttw")

            res_by_channel_name = await self.api.get_channel_info(
                for_username="GoogleDevelopers", return_json=True
            )
            self.assertEqual(
                res_by_channel_name["items"][0]["id"], "UC_x5XG1OV2P6uZZ5FSM9Ttw"
            )

            res_by_mine = await self.api.get_channel_info(mine=True)
            self.assertEqual(res_by_mine.items[0].id, "UC_x5XG1OV2P6uZZ5FSM9Ttw")

        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL, json=self.CHANNELS_INFO_MULTI)

            res_by_channel_id_list = await self.api.get_channel_info(
                channel_id="UC_x5XG1OV2P6uZZ5FSM9Ttw,UCK8sQmJBp8GCxrOtXWBpyEA",
                parts="id,snippet",
            )
            self.assertEqual(len(res_by_channel_id_list.items), 2)
            self.assertEqual(
                res_by_channel_id_list.items[1].id, "UCK8sQmJBp8GCxrOtXWBpyEA"
            )
