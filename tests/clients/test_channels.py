import pytest
import responses

from .base import BaseTestCase
from pyyoutube.error import PyYouTubeException
import pyyoutube.models as mds


class TestChannelsResource(BaseTestCase):
    RESOURCE = "channels"
    channel_id = "UC_x5XG1OV2P6uZZ5FSM9Ttw"

    def test_list(self, helpers, authed_cli, key_cli):
        with pytest.raises(PyYouTubeException):
            key_cli.channels.list()

        with responses.RequestsMock() as m:
            m.add(
                method="GET",
                url=self.url,
                json=self.load_json("channels/info.json", helpers),
            )

            res = key_cli.channels.list(
                parts="id,snippet",
                channel_id=self.channel_id,
            )
            assert res.items[0].id == self.channel_id
            assert key_cli.channels.api_key == "api key"

            res = key_cli.channels.list(
                parts="id,snippet",
                for_handle="@googledevelopers",
            )
            assert res.items[0].snippet.customUrl == "@googledevelopers"

            res = key_cli.channels.list(
                parts=["id", "snippet"], for_username="googledevelopers"
            )
            assert res.items[0].snippet.title == "Google Developers"

            res = authed_cli.channels.list(
                parts=("id", "snippet"),
                managed_by_me=True,
            )
            assert res.items[0].snippet.title == "Google Developers"

            res = authed_cli.channels.list(
                parts={"id", "snippet"},
                mine=True,
            )
            assert res.items[0].snippet.title == "Google Developers"

        with responses.RequestsMock() as m:
            m.add(
                method="GET",
                url=self.url,
                json=self.load_json("channels/info_multiple.json", helpers),
            )

            res = authed_cli.channels.list(
                parts="id,snippet,statistics,contentDetails,brandingSettings",
                channel_id="UC_x5XG1OV2P6uZZ5FSM9Ttw,UCK8sQmJBp8GCxrOtXWBpyEA",
            )
            assert len(res.items) == 2

    def test_update(self, helpers, authed_cli):
        with responses.RequestsMock() as m:
            m.add(
                method="PUT",
                url=self.url,
                json=self.load_json("channels/update_resp.json", helpers),
            )

            updated_channel = authed_cli.channels.update(
                part="brandingSettings",
                body=mds.Channel(
                    brandingSettings=mds.ChannelBrandingSetting(
                        channel=mds.ChannelBrandingSettingChannel(
                            title="ikaros data",
                            description="This is a test channel.",
                            keywords="life 学习 测试",
                            country="CN",
                            defaultLanguage="en",
                        )
                    )
                ),
            )
            assert updated_channel.brandingSettings.channel.defaultLanguage == "en"
