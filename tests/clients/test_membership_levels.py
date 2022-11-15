import responses

from .base import BaseTestCase


class TestMembershipLevelsResource(BaseTestCase):
    RESOURCE = "membershipsLevels"

    def test_list(self, helpers, authed_cli):
        with responses.RequestsMock() as m:
            m.add(
                method="GET",
                url=self.url,
                json=self.load_json("members/membership_levels.json", helpers),
            )

            res = authed_cli.membershipsLevels.list(
                parts=["id", "snippet"],
            )
            assert len(res.items) == 2
