import responses

from .base import BaseTestCase


class TestChannelsResource(BaseTestCase):
    RESOURCE = "channels"
    channel_id = "UC_x5XG1OV2P6uZZ5FSM9Ttw"

    def test_list(self, helpers, authed_cli):
        with responses.RequestsMock() as m:
            m.add(
                method="GET",
                url=self.url,
                json=self.load_json("channel_info_single.json", helpers),
            )

            res = authed_cli.channels.list(
                parts="id,snippet,statistics",
                id=self.channel_id,
            )
            assert res.items[0].id == self.channel_id

        with responses.RequestsMock() as m:
            m.add(
                method="GET",
                url=self.url,
                json=self.load_json("channel_info_multi.json", helpers),
            )

            res = authed_cli.channels.list(
                parts=["id", "snippet", "statistics"],
                id="UC_x5XG1OV2P6uZZ5FSM9Ttw,UCK8sQmJBp8GCxrOtXWBpyEA",
            )
            assert len(res.items) == 2
