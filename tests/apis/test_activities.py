import json
import unittest

import responses

import pyyoutube


class ApiActivitiesTest(unittest.TestCase):
    BASE_PATH = "testdata/apidata/activities/"
    BASE_URL = "https://www.googleapis.com/youtube/v3/activities"

    with open(BASE_PATH + "activities_by_channel_p1.json", "rb") as f:
        ACTIVITIES_CHANNEL_P1 = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "activities_by_channel_p2.json", "rb") as f:
        ACTIVITIES_CHANNEL_P2 = json.loads(f.read().decode("utf-8"))

    with open(BASE_PATH + "activities_by_mine_p1.json", "rb") as f:
        ACTIVITIES_MINE_P1 = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "activities_by_mine_p2.json", "rb") as f:
        ACTIVITIES_MINE_P2 = json.loads(f.read().decode("utf-8"))

    def setUp(self) -> None:
        self.api = pyyoutube.Api(api_key="api key")
        self.api_with_access_token = pyyoutube.Api(access_token="token")

    def testGetChannelActivities(self) -> None:
        # test parts
        with self.assertRaises(pyyoutube.PyYouTubeException):
            self.api.get_activities_by_channel(channel_id="id", parts="id,not_part")

        # test get all activities
        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL, json=self.ACTIVITIES_CHANNEL_P1)
            m.add("GET", self.BASE_URL, json=self.ACTIVITIES_CHANNEL_P2)

            res = self.api.get_activities_by_channel(
                channel_id="UC_x5XG1OV2P6uZZ5FSM9Ttw",
                parts="id,snippet",
                before="2019-11-1T00:00:00.000Z",
                after="2019-10-1T00:00:00.000Z",
                region_code="US",
                count=None,
            )
            self.assertEqual(len(res.items), 13)

        # test get by page token
        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL, json=self.ACTIVITIES_CHANNEL_P2)

            res = self.api.get_activities_by_channel(
                channel_id="UC_x5XG1OV2P6uZZ5FSM9Ttw",
                parts="id,snippet",
                count=None,
                page_token="CAoQAA",
                return_json=True,
            )
            self.assertEqual(len(res["items"]), 3)

    def testGetMineActivities(self) -> None:
        # test parts
        with self.assertRaises(pyyoutube.PyYouTubeException):
            self.api_with_access_token.get_activities_by_me(parts="id,not_part")

        # test get all activities
        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL, json=self.ACTIVITIES_MINE_P1)
            m.add("GET", self.BASE_URL, json=self.ACTIVITIES_MINE_P2)

            res = self.api_with_access_token.get_activities_by_me(
                parts="id,snippet",
                before="2019-11-1T00:00:00.000Z",
                after="2019-12-1T00:00:00.000Z",
                region_code="US",
                count=None,
            )
            self.assertEqual(len(res.items), 2)

        # test page token
        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL, json=self.ACTIVITIES_MINE_P2)

            res = self.api_with_access_token.get_activities_by_me(
                parts="id,snippet",
                before="2019-11-1T00:00:00.000Z",
                after="2019-12-1T00:00:00.000Z",
                region_code="US",
                page_token="CAEQAA",
                count=None,
                return_json=True,
            )
            self.assertEqual(len(res["items"]), 1)
