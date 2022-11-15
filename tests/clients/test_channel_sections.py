import pytest
import responses

import pyyoutube.models as mds
from .base import BaseTestCase
from pyyoutube.error import PyYouTubeException


class TestChannelBannersResource(BaseTestCase):
    RESOURCE = "channelSections"

    def test_list(self, helpers, authed_cli, key_cli):
        with pytest.raises(PyYouTubeException):
            key_cli.channelSections.list()

        with responses.RequestsMock() as m:
            m.add(
                method="GET",
                url=self.url,
                json=self.load_json(
                    "channel_sections/channel_sections_by_channel.json", helpers
                ),
            )

            res = key_cli.channelSections.list(
                parts=["id", "snippet"],
                channel_id="UCa-vrCLQHviTOVnEKDOdetQ",
            )
            assert res.items[0].snippet.type == "recentUploads"

            res = authed_cli.channelSections.list(
                mine=True,
                parts=["id", "snippet"],
            )
            assert res.items[0].snippet.channelId == "UCa-vrCLQHviTOVnEKDOdetQ"

        with responses.RequestsMock() as m:
            m.add(
                method="GET",
                url=self.url,
                json=self.load_json(
                    "channel_sections/channel_sections_by_id.json", helpers
                ),
            )
            res = key_cli.channelSections.list(
                parts=["id", "snippet"],
                section_id="UCa-vrCLQHviTOVnEKDOdetQ.nGzAI5pLbMY",
            )
            assert res.items[0].snippet.type == "multiplePlaylists"

    def test_insert(self, helpers, authed_cli):
        with responses.RequestsMock() as m:
            m.add(
                method="POST",
                url=self.url,
                json=self.load_json("channel_sections/insert_resp.json", helpers),
            )
            section = authed_cli.channelSections.insert(
                parts="id,snippet,contentDetails",
                body=mds.ChannelSection(
                    snippet=mds.ChannelSectionSnippet(
                        type="multiplePlaylists",
                        position=4,
                    ),
                    contentDetails=mds.ChannelSectionContentDetails(
                        playlists=["PLBaidt0ilCMbUdj0EppB710c_X5OuCP2g"]
                    ),
                ),
            )
            assert section.id == "UCa-vrCLQHviTOVnEKDOdetQ.Zx4DA4xg9IM"

    def test_update(self, helpers, authed_cli):
        with responses.RequestsMock() as m:
            m.add(
                method="PUT",
                url=self.url,
                json=self.load_json("channel_sections/insert_resp.json", helpers),
            )
            section = authed_cli.channelSections.update(
                parts="id,snippet,contentDetails",
                body=mds.ChannelSection(
                    id="UCa-vrCLQHviTOVnEKDOdetQ.Zx4DA4xg9IM",
                    snippet=mds.ChannelSectionSnippet(
                        type="multiplePlaylists",
                        position=4,
                    ),
                ),
            )
            assert section.id == "UCa-vrCLQHviTOVnEKDOdetQ.Zx4DA4xg9IM"

    def test_delete(self, helpers, authed_cli):
        with responses.RequestsMock() as m:
            m.add(
                method="DELETE",
                url=self.url,
            )
            assert authed_cli.channelSections.delete(
                section_id="UCa-vrCLQHviTOVnEKDOdetQ.Zx4DA4xg9IM"
            )

        with pytest.raises(PyYouTubeException):
            with responses.RequestsMock() as m:
                m.add(
                    method="DELETE",
                    url=self.url,
                    json=self.load_json("error_permission_resp.json", helpers),
                    status=403,
                )
                authed_cli.channelSections.delete(
                    section_id="UCa-vrCLQHviTOVnEKDOdetQ.Zx4DA4xg9IM"
                )
