import pytest
import responses

import pyyoutube.models as mds
from .base import BaseTestCase
from pyyoutube.error import PyYouTubeException


class TestSubscriptionsResource(BaseTestCase):
    RESOURCE = "subscriptions"

    def test_list(self, helpers, key_cli, authed_cli):
        with pytest.raises(PyYouTubeException):
            key_cli.subscriptions.list()

        with responses.RequestsMock() as m:
            m.add(
                method="GET",
                url=self.url,
                json=self.load_json(
                    "subscriptions/subscriptions_by_mine_p1.json", helpers
                ),
            )

            res = key_cli.subscriptions.list(
                parts=["id", "snippet"],
                channel_id="UCa-vrCLQHviTOVnEKDOdetQ",
                max_results=10,
            )
            assert res.items[0].id == "zqShTXi-2-Tx7TtwQqhCBzrqBvZj94YvFZOGA9x6NuY"

            res = authed_cli.subscriptions.list(mine=True, max_results=10)
            assert res.items[0].snippet.channelId == "UCNvMBmCASzTNNX8lW3JRMbw"

            res = authed_cli.subscriptions.list(
                my_recent_subscribers=True, max_results=10
            )
            assert res.items[0].snippet.channelId == "UCNvMBmCASzTNNX8lW3JRMbw"

            res = authed_cli.subscriptions.list(my_subscribers=True, max_results=10)
            assert res.items[0].snippet.channelId == "UCNvMBmCASzTNNX8lW3JRMbw"

        with responses.RequestsMock() as m:
            m.add(
                method="GET",
                url=self.url,
                json=self.load_json("subscriptions/subscriptions_by_id.json", helpers),
            )
            res = key_cli.subscriptions.list(
                parts=["id", "snippet"],
                subscription_id=[
                    "zqShTXi-2-Tx7TtwQqhCBwViE_j9IEgnmRmPnqJljxo",
                    "zqShTXi-2-Rya5uUxEp3ZsPI3fZrFQnSXNQCwvHBGGo",
                ],
            )
            assert res.items[0].id == "zqShTXi-2-Tx7TtwQqhCBwViE_j9IEgnmRmPnqJljxo"

    def test_inset(self, helpers, authed_cli):
        with responses.RequestsMock() as m:
            m.add(
                method="POST",
                url=self.url,
                json=self.load_json("subscriptions/insert_response.json", helpers),
            )
            subscription = authed_cli.subscriptions.insert(
                body=mds.Subscription(
                    snippet=mds.SubscriptionSnippet(
                        resourceId=mds.ResourceId(
                            kind="youtube#channel",
                            channelId="UCQ6ptCagG3W0Bf4lexvnBEg",
                        )
                    )
                )
            )
            assert subscription.id == "POsnRIYsMcp1Cghr_Fsh-6uFZRcIHmTKzzByiv9ZAro"

    def test_delete(self, helpers, authed_cli):
        with responses.RequestsMock() as m:
            m.add(
                method="DELETE",
                url=self.url,
                status=204,
            )
            assert authed_cli.subscriptions.delete(
                subscription_id="POsnRIYsMcp1Cghr_Fsh-6uFZRcIHmTKzzByiv9ZAro"
            )

        with pytest.raises(PyYouTubeException):
            with responses.RequestsMock() as m:
                m.add(
                    method="DELETE",
                    url=self.url,
                    json=self.load_json("error_permission_resp.json", helpers),
                    status=403,
                )
                authed_cli.subscriptions.delete(
                    subscription_id="POsnRIYsMcp1Cghr_Fsh-6uFZRcIHmTKzzByiv9ZAro"
                )
