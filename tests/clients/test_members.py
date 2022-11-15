import responses

from .base import BaseTestCase


class TestMembersResource(BaseTestCase):
    RESOURCE = "members"

    def test_list(self, helpers, authed_cli):
        with responses.RequestsMock() as m:
            m.add(
                method="GET",
                url=self.url,
                json=self.load_json("members/members_data.json", helpers),
            )

            res = authed_cli.members.list(
                parts=["snippet"],
                mode="all_current",
                max_results=5,
            )
            assert len(res.items) == 2
