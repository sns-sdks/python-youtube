import pytest
import responses

from .base import BaseTestCase
from pyyoutube.error import PyYouTubeException


class TestActivitiesResource(BaseTestCase):
    RESOURCE = "activities"

    def test_list(self, helpers, authed_cli):
        with pytest.raises(PyYouTubeException):
            authed_cli.activities.list()

        with responses.RequestsMock() as m:
            m.add(
                method="GET",
                url=self.url,
                json=self.load_json(
                    "activities/activities_by_channel_p1.json", helpers
                ),
            )
            res = authed_cli.activities.list(
                parts=["id", "snippet"],
                channel_id="UC_x5XG1OV2P6uZZ5FSM9Ttw",
                max_results=10,
            )
            assert len(res.items) == 10
            assert authed_cli.activities.access_token == "access token"

            res = authed_cli.activities.list(
                parts=["id", "snippet"], mine=True, max_results=10
            )
            assert res.items[0].snippet.type == "upload"
