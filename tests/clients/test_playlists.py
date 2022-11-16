import pytest
import responses

import pyyoutube.models as mds
from .base import BaseTestCase
from pyyoutube.error import PyYouTubeException


class TestPlaylistsResource(BaseTestCase):
    RESOURCE = "playlists"

    def test_list(self, helpers, authed_cli, key_cli):
        with pytest.raises(PyYouTubeException):
            authed_cli.playlists.list()

        with responses.RequestsMock() as m:
            m.add(
                method="GET",
                url=self.url,
                json=self.load_json("playlists/playlists_paged_1.json", helpers),
            )

            res = key_cli.playlists.list(
                parts=["id", "snippet"],
                channel_id="UC_x5XG1OV2P6uZZ5FSM9Ttw",
                max_results=10,
            )
            assert len(res.items) == 10

            res = key_cli.playlists.list(
                parts=["id", "snippet"],
                playlist_id=[
                    "PLOU2XLYxmsIKpaV8h0AGE05so0fAwwfTw",
                    "PLOU2XLYxmsIJO83u2UmyC8ud41AvUnhgj",
                ],
            )
            assert res.items[0].id == "PLOU2XLYxmsIKpaV8h0AGE05so0fAwwfTw"

            res = authed_cli.playlists.list(
                parts=["id", "snippet"], mine=True, max_results=10
            )
            assert len(res.items) == 10

    def test_insert(self, helpers, authed_cli):
        with responses.RequestsMock() as m:
            m.add(
                method="POST",
                url=self.url,
                json=self.load_json("playlists/insert_response.json", helpers),
            )

            playlist = authed_cli.playlists.insert(
                body=mds.Playlist(
                    snippet=mds.PlaylistSnippet(
                        title="Test playlist",
                    )
                ),
            )

            assert playlist.id == "PLBaidt0ilCMZN8XPVB5iXY6FlSYGeyn2n"

    def test_update(self, helpers, authed_cli):
        with responses.RequestsMock() as m:
            m.add(
                method="PUT",
                url=self.url,
                json=self.load_json("playlists/insert_response.json", helpers),
            )

            playlist = authed_cli.playlists.update(
                body=mds.Playlist(
                    snippet=mds.PlaylistSnippet(
                        title="Test playlist",
                        defaultLanguage="",
                    )
                )
            )
            assert playlist.snippet.description == ""

    def test_delete(self, helpers, authed_cli):
        with responses.RequestsMock() as m:
            m.add(method="DELETE", url=self.url, status=204)

            assert authed_cli.playlists.delete(
                playlist_id="PLBaidt0ilCMZN8XPVB5iXY6FlSYGeyn2n"
            )

        with pytest.raises(PyYouTubeException):
            with responses.RequestsMock() as m:
                m.add(
                    method="DELETE",
                    url=self.url,
                    json=self.load_json("error_permission_resp.json", helpers),
                    status=403,
                )
                authed_cli.playlists.delete(
                    playlist_id="PLBaidt0ilCMZN8XPVB5iXY6FlSYGeyn2n"
                )
