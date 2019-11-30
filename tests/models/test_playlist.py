import json
import unittest

import pyyoutube.models as models


class PlaylistModelTest(unittest.TestCase):
    BASE_PATH = "testdata/modeldata/playlists/"

    with open(BASE_PATH + "playlist_content_details.json", "rb") as f:
        CONTENT_DETAILS_INFO = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "playlist_snippet.json", "rb") as f:
        SNIPPET_INFO = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "playlist_status.json", "rb") as f:
        STATUS_INFO = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "playlist_info.json", "rb") as f:
        PLAYLIST_INFO = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "playlist_api_response.json", "rb") as f:
        PLAYLIST_RESPONSE_INFO = json.loads(f.read().decode("utf-8"))

    def testPlayListContentDetails(self) -> None:
        m = models.PlaylistContentDetails.from_dict(self.CONTENT_DETAILS_INFO)

        self.assertEqual(m.itemCount, 4)

    def testPlayListSnippet(self) -> None:
        m = models.PlaylistSnippet.from_dict(self.SNIPPET_INFO)

        self.assertEqual(
            m.string_to_datetime(m.publishedAt).isoformat(), "2019-05-16T18:46:20+00:00"
        )
        self.assertEqual(m.title, "Assistant on Air")
        self.assertEqual(
            m.thumbnails.default.url, "https://i.ytimg.com/vi/D-lhorsDlUQ/default.jpg"
        )
        self.assertEqual(m.localized.title, "Assistant on Air")

    def testPlayListStatus(self) -> None:
        m = models.PlaylistStatus.from_dict(self.STATUS_INFO)

        self.assertEqual(m.privacyStatus, "public")

    def testPlayList(self) -> None:
        m = models.Playlist.from_dict(self.PLAYLIST_INFO)

        self.assertEqual(m.id, "PLOU2XLYxmsIJpufeMHncnQvFOe0K3MhVp")
        self.assertEqual(m.player, None)
        self.assertEqual(m.snippet.title, "Assistant on Air")

    def testPlaylistListResponse(self) -> None:
        m = models.PlaylistListResponse.from_dict(self.PLAYLIST_RESPONSE_INFO)

        self.assertEqual(m.kind, "youtube#playlistListResponse")
        self.assertEqual(m.pageInfo.totalResults, 416)
        self.assertEqual(m.items[0].id, "PLOU2XLYxmsIJpufeMHncnQvFOe0K3MhVp")
