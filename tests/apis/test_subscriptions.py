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
    with open(BASE_PATH + "subscriptions_by_channel_p1.json", "rb") as f:
        SUBSCRIPTIONS_BY_CHANNEL_P1 = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "subscriptions_by_channel_p2.json", "rb") as f:
        SUBSCRIPTIONS_BY_CHANNEL_P2 = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "subscriptions_by_channel_with_filter.json", "rb") as f:
        SUBSCRIPTIONS_BY_CHANNEL_FILTER = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "subscriptions_by_mine_p1.json", "rb") as f:
        SUBSCRIPTIONS_BY_MINE_P1 = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "subscriptions_by_mine_p2.json", "rb") as f:
        SUBSCRIPTIONS_BY_MINE_P2 = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "subscriptions_by_mine_filter.json", "rb") as f:
        SUBSCRIPTIONS_BY_MINE_FILTER = json.loads(f.read().decode("utf-8"))

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
                subscription_id=(
                    "zqShTXi-2-Tx7TtwQqhCBwViE_j9IEgnmRmPnqJljxo,"
                    "zqShTXi-2-Rya5uUxEp3ZsPI3fZrFQnSXNQCwvHBGGo"
                ),
                parts="id,snippet",
                return_json=True,
            )
            self.assertEqual(len(res_zero["items"]), 0)
            self.assertEqual(res_zero["pageInfo"]["totalResults"], 0)

            res_by_id = self.api_with_access_token.get_subscription_by_id(
                subscription_id=[
                    "zqShTXi-2-Tx7TtwQqhCBwViE_j9IEgnmRmPnqJljxo",
                    "zqShTXi-2-Rya5uUxEp3ZsPI3fZrFQnSXNQCwvHBGGo",
                ],
                parts="id,snippet",
            )
            self.assertEqual(len(res_by_id.items), 2)
            self.assertEqual(res_by_id.pageInfo.totalResults, 2)
            self.assertEqual(
                res_by_id.items[0].id, "zqShTXi-2-Tx7TtwQqhCBwViE_j9IEgnmRmPnqJljxo"
            )

    def testGetSubscriptionByChannel(self) -> None:
        # test params checker
        with self.assertRaises(pyyoutube.PyYouTubeException):
            self.api_with_access_token.get_subscription_by_channel(
                channel_id="id", parts="id,not_part"
            )

        # test count is None
        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL, json=self.SUBSCRIPTIONS_BY_CHANNEL_P1)
            m.add("GET", self.BASE_URL, json=self.SUBSCRIPTIONS_BY_CHANNEL_P2)

            res = self.api.get_subscription_by_channel(
                channel_id="UCAuUUnT6oDeKwE6v1NGQxug",
                count=None,
                limit=5,
            )

            self.assertEqual(len(res.items), 7)

        # test count
        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL, json=self.SUBSCRIPTIONS_BY_CHANNEL_P1)

            res = self.api.get_subscription_by_channel(
                channel_id="UCAuUUnT6oDeKwE6v1NGQxug",
                count=5,
                limit=5,
            )

            self.assertEqual(len(res.items), 5)

        # test filter
        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL, json=self.SUBSCRIPTIONS_BY_CHANNEL_P1)

            res = self.api.get_subscription_by_channel(
                channel_id="UCAuUUnT6oDeKwE6v1NGQxug",
                for_channel_id=["UCsT0YIqwnpJCM-mx7-gSA4Q", "UCtC8aQzdEHAmuw8YvtH1CcQ"],
                count=2,
                return_json=True,
            )

            self.assertEqual(len(res["items"]), 2)

        # test use page token
        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL, json=self.SUBSCRIPTIONS_BY_CHANNEL_P2)

            res = self.api.get_subscription_by_channel(
                channel_id="UCAuUUnT6oDeKwE6v1NGQxug",
                count=None,
                limit=5,
                page_token="CAUQAA",
            )

            self.assertEqual(len(res.items), 2)

    def testGetSubscriptionByMe(self) -> None:
        # test not have required parameters
        with self.assertRaises(pyyoutube.PyYouTubeException):
            self.api_with_access_token.get_subscription_by_me()

        # test get all data
        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL, json=self.SUBSCRIPTIONS_BY_MINE_P1)
            m.add("GET", self.BASE_URL, json=self.SUBSCRIPTIONS_BY_MINE_P2)

            sub = self.api_with_access_token.get_subscription_by_me(
                mine=True,
                parts=["id", "snippet"],
                order="alphabetically",
                count=None,
                limit=10,
            )

            self.assertEqual(len(sub.items), 15)
            self.assertEqual(sub.pageInfo.totalResults, 16)
            # totalResults is only an approximation/estimate.
            # Refer: https://stackoverflow.com/questions/43507281/totalresults-count-doesnt-match-with-the-actual-results-returned-in-youtube-v3

        # test count
        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL, json=self.SUBSCRIPTIONS_BY_MINE_P1)

            sub = self.api_with_access_token.get_subscription_by_me(
                mine=True,
                parts="id,snippet",
                order="alphabetically",
                count=5,
                limit=10,
                return_json=True,
            )

            self.assertEqual(len(sub["items"]), 5)
            self.assertEqual(sub["pageInfo"]["totalResults"], 16)

        # test filter channel id
        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL, json=self.SUBSCRIPTIONS_BY_MINE_FILTER)

            sub = self.api_with_access_token.get_subscription_by_me(
                mine=True,
                parts="id,snippet",
                for_channel_id="UC_x5XG1OV2P6uZZ5FSM9Ttw,UCa-vrCLQHviTOVnEKDOdetQ",
                count=None,
            )

            self.assertEqual(len(sub.items), 2)
            self.assertEqual(sub.pageInfo.totalResults, 2)

        # test remain
        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL, json=self.SUBSCRIPTIONS_ZERO)

            recent = self.api_with_access_token.get_subscription_by_me(
                recent_subscriber=True
            )
            self.assertEqual(len(recent.items), 0)

            subscriber = self.api_with_access_token.get_subscription_by_me(
                subscriber=True
            )
            self.assertEqual(len(subscriber.items), 0)

        # test get all data
        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL, json=self.SUBSCRIPTIONS_BY_MINE_P2)

            sub = self.api_with_access_token.get_subscription_by_me(
                mine=True,
                parts=["id", "snippet"],
                order="alphabetically",
                count=None,
                limit=10,
                page_token="CAoQAA",
            )

            self.assertEqual(len(sub.items), 6)
