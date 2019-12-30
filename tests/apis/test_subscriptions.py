import json
import unittest

import responses

import pyyoutube


class ApiPlaylistTest(unittest.TestCase):
    BASE_PATH = "testdata/apidata/subscriptions/"
    BASE_URL = "https://www.googleapis.com/youtube/v3/subscriptions"

    with open(BASE_PATH + "subscription_zero.json", "rb") as f:
        SUBSCRIPTIONS_ZERO = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "subscriptions_by_id.json", "rb") as f:
        SUBSCRIPTIONS_BY_ID = json.loads(f.read().decode("utf-8"))

    def setUp(self) -> None:
        self.api = pyyoutube.Api(api_key="api key")
        self.api_with_access_token = pyyoutube.Api(access_token="access token")

    def testGetSubscriptionById(self) -> None:
        # test params checker
        with self.assertRaises(pyyoutube.PyYouTubeException):
            self.api_with_access_token.get_subscription_by_id(
                subscription_id="id", parts="id,not_part"
            )

        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL, json=self.SUBSCRIPTIONS_ZERO)
            m.add("GET", self.BASE_URL, json=self.SUBSCRIPTIONS_BY_ID)

            res_zero = self.api.get_subscription_by_id(
                subscription_id="zqShTXi-2-Tx7TtwQqhCBwViE_j9IEgnmRmPnqJljxo,"
                "zqShTXi-2-Rya5uUxEp3ZsPI3fZrFQnSXNQCwvHBGGo",
                parts="id,snippet",
                return_json=True,
            )
            self.assertEqual(len(res_zero["items"]), 0)
            self.assertEqual(res_zero["pageInfo"]["totalResults"], 0)

            res_by_id = self.api_with_access_token.get_subscription_by_id(
                subscription_id="zqShTXi-2-Tx7TtwQqhCBwViE_j9IEgnmRmPnqJljxo,"
                "zqShTXi-2-Rya5uUxEp3ZsPI3fZrFQnSXNQCwvHBGGo",
                parts="id,snippet",
            )
            self.assertEqual(len(res_by_id.items), 2)
            self.assertEqual(res_by_id.pageInfo.totalResults, 2)
            self.assertEqual(
                res_by_id.items[0].id, "zqShTXi-2-Tx7TtwQqhCBwViE_j9IEgnmRmPnqJljxo"
            )
