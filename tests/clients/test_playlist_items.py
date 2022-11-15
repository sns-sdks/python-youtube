import pytest
import responses

import pyyoutube.models as mds
from .base import BaseTestCase
from pyyoutube.error import PyYouTubeException


class TestPlaylistItemsResource(BaseTestCase):
    RESOURCE = "playlistItems"

    def test_list(self, helpers, key_cli):
        with pytest.raises(PyYouTubeException):
            key_cli.playlistItems.list()

        with responses.RequestsMock() as m:
            m.add(
                method="GET",
                url=self.url,
                json=self.load_json(
                    "playlist_items/playlist_items_paged_1.json", helpers
                ),
            )

            res = key_cli.playlistItems.list(
                parts=["id", "snippet"],
                playlist_id="PLOU2XLYxmsIKpaV8h0AGE05so0fAwwfTw",
                max_results=10,
            )
            assert len(res.items) == 10

            res = key_cli.playlistItems.list(
                playlist_item_id="UExPVTJYTFl4bXNJS3BhVjhoMEFHRTA1c28wZkF3d2ZUdy41NkI0NEY2RDEwNTU3Q0M2",
                parts=["id", "snippet"],
            )
            assert (
                res.items[0].id
                == "UExPVTJYTFl4bXNJS3BhVjhoMEFHRTA1c28wZkF3d2ZUdy41NkI0NEY2RDEwNTU3Q0M2"
            )

    def test_insert(self, helpers, authed_cli):
        with responses.RequestsMock() as m:
            m.add(
                method="POST",
                url=self.url,
                json=self.load_json("playlist_items/insert_response.json", helpers),
            )

            item = authed_cli.playlistItems.insert(
                body=mds.PlaylistItem(
                    snippet=mds.PlaylistItemSnippet(
                        playlistId="PLBaidt0ilCManGDIKr8UVBFZwN_UvMKvS",
                        position=0,
                        resourceId=mds.ResourceId(
                            kind="youtube#video", videoId="2sjqTHE0zok"
                        ),
                    )
                ),
                parts=["id", "snippet"],
            )
            assert item.snippet.playlistId == "PLBaidt0ilCManGDIKr8UVBFZwN_UvMKvS"

    def test_update(self, helpers, authed_cli):
        with responses.RequestsMock() as m:
            m.add(
                method="PUT",
                url=self.url,
                json=self.load_json("playlist_items/insert_response.json", helpers),
            )

            item = authed_cli.playlistItems.update(
                body=mds.PlaylistItem(
                    snippet=mds.PlaylistItemSnippet(
                        playlistId="PLBaidt0ilCManGDIKr8UVBFZwN_UvMKvS",
                        position=1,
                        resourceId=mds.ResourceId(
                            kind="youtube#video", videoId="2sjqTHE0zok"
                        ),
                    )
                ),
                parts=["id", "snippet"],
            )
            assert item.snippet.playlistId == "PLBaidt0ilCManGDIKr8UVBFZwN_UvMKvS"

    def test_delete(self, helpers, authed_cli):
        with responses.RequestsMock() as m:
            m.add(method="DELETE", url=self.url, status=204)
            assert authed_cli.playlistItems.delete(
                playlist_item_id="PLBaidt0ilCManGDIKr8UVBFZwN_UvMKvSxxxxx"
            )

        with pytest.raises(PyYouTubeException):
            with responses.RequestsMock() as m:
                m.add(
                    method="DELETE",
                    url=self.url,
                    json=self.load_json("error_permission_resp.json", helpers),
                    status=403,
                )
                authed_cli.playlistItems.delete(playlist_item_id="xxxxxx")
