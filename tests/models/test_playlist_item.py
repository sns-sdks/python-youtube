import json
import unittest

import pyyoutube.models as models


class PlaylistItemModelTest(unittest.TestCase):
    BASE_PATH = "testdata/modeldata/playlist_items/"

    with open(BASE_PATH + "playlist_item_content_details.json", "rb") as f:
        CONTENT_DETAILS_INFO = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "playlist_item_snippet.json", "rb") as f:
        SNIPPET_INFO = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "playlist_item_status.json", "rb") as f:
        STATUS_INFO = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "playlist_item_info.json", "rb") as f:
        PLAYLIST_ITEM_INFO = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "playlist_item_api_response.json", "rb") as f:
        PLAYLIST_LIST_RESPONSE = json.loads(f.read().decode("utf-8"))

    def testPlaylistItemContentDetails(self) -> None:
        m = models.PlaylistItemContentDetails.from_dict(self.CONTENT_DETAILS_INFO)

        self.assertEqual(m.videoId, "D-lhorsDlUQ")
        self.assertEqual(
            m.string_to_datetime(m.videoPublishedAt).isoformat(),
            "2019-03-21T20:37:49+00:00",
        )

    def testPlaylistItemSnippet(self) -> None:
        m = models.PlaylistItemSnippet.from_dict(self.SNIPPET_INFO)

        self.assertEqual(
            m.string_to_datetime(m.publishedAt).isoformat(), "2019-05-16T18:46:20+00:00"
        )
        self.assertEqual(m.title, "What are Actions on Google (Assistant on Air)")
        self.assertEqual(
            m.thumbnails.default.url, "https://i.ytimg.com/vi/D-lhorsDlUQ/default.jpg"
        )
        self.assertEqual(m.resourceId.videoId, "D-lhorsDlUQ")

    def testPlaylistItemStatus(self) -> None:
        m = models.PlaylistItemStatus.from_dict(self.STATUS_INFO)

        self.assertEqual(m.privacyStatus, "public")

    def testPlaylistItem(self) -> None:
        m = models.PlaylistItem.from_dict(self.PLAYLIST_ITEM_INFO)

        self.assertEqual(
            m.id, "UExPVTJYTFl4bXNJSnB1ZmVNSG5jblF2Rk9lMEszTWhWcC41NkI0NEY2RDEwNTU3Q0M2"
        )
        self.assertEqual(m.snippet.channelId, "UC_x5XG1OV2P6uZZ5FSM9Ttw")
        self.assertEqual(m.snippet.resourceId.videoId, "D-lhorsDlUQ")
        self.assertEqual(m.contentDetails.videoId, "D-lhorsDlUQ")
        self.assertEqual(m.status.privacyStatus, "public")
        self.assertEqual(m.snippet.videoOwnerChannelId, "UC_x5XG1OV2P6uZZ5FSM9Ttw")

    def testPlaylistItemListResponse(self) -> None:
        m = models.PlaylistItemListResponse.from_dict(self.PLAYLIST_LIST_RESPONSE)

        self.assertEqual(m.kind, "youtube#playlistItemListResponse")
        self.assertEqual(m.pageInfo.totalResults, 3)
        self.assertEqual(len(m.items), 3)
        self.assertEqual(
            m.items[0].id,
            "UExPVTJYTFl4bXNJSlhzSDJodEcxZzBOVWpIR3E2MlE3aS41NkI0NEY2RDEwNTU3Q0M2",
        )
