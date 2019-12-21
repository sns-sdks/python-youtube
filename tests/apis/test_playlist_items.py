import json
import unittest

import responses

import pyyoutube


class ApiPlaylistItemTest(unittest.TestCase):
    BASE_PATH = "testdata/apidata/playlist_items/"
    BASE_URL = "https://www.googleapis.com/youtube/v3/playlistItems"

    with open(BASE_PATH + "playlist_items_single.json", "rb") as f:
        PLAYLIST_ITEM_INFO_SINGLE = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "playlist_items_multi.json", "rb") as f:
        PLAYLIST_ITEM_INFO_MULTI = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "playlist_items_paged_1.json", "rb") as f:
        PLAYLIST_ITEM_PAGED_1 = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "playlist_items_paged_2.json", "rb") as f:
        PLAYLIST_ITEM_PAGED_2 = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "playlist_items_filter_video.json", "rb") as f:
        PLAYLIST_ITEM_FILTER = json.loads(f.read().decode("utf-8"))

    def setUp(self) -> None:
        self.api = pyyoutube.Api(api_key="api key")

    def testGetPlaylistItemById(self) -> None:
        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL, json=self.PLAYLIST_ITEM_INFO_SINGLE)
            m.add("GET", self.BASE_URL, json=self.PLAYLIST_ITEM_INFO_MULTI)

            res_by_single_id = self.api.get_playlist_item_by_id(
                playlist_item_id="UExPVTJYTFl4bXNJSlhzSDJodEcxZzBOVWpIR3E2MlE3aS41NkI0NEY2RDEwNTU3Q0M2",
                parts="id,snippet",
                return_json=True,
            )
            self.assertEqual(
                res_by_single_id["kind"], "youtube#playlistItemListResponse"
            )
            self.assertEqual(
                res_by_single_id["items"][0]["id"],
                "UExPVTJYTFl4bXNJSlhzSDJodEcxZzBOVWpIR3E2MlE3aS41NkI0NEY2RDEwNTU3Q0M2",
            )

            res_by_multi_id = self.api.get_playlist_item_by_id(
                playlist_item_id=[
                    "UExPVTJYTFl4bXNJSlhzSDJodEcxZzBOVWpIR3E2MlE3aS41NkI0NEY2RDEwNTU3Q0M2",
                    "UExPVTJYTFl4bXNJSlhzSDJodEcxZzBOVWpIR3E2MlE3aS4yODlGNEE0NkRGMEEzMEQy",
                ],
                parts=["id", "snippet"],
            )
            self.assertEqual(res_by_multi_id.pageInfo.totalResults, 2)
            self.assertEqual(len(res_by_multi_id.items), 2)
            self.assertEqual(
                res_by_multi_id.items[1].id,
                "UExPVTJYTFl4bXNJSlhzSDJodEcxZzBOVWpIR3E2MlE3aS4yODlGNEE0NkRGMEEzMEQy",
            )

    def testGetPlaylistItems(self) -> None:
        with self.assertRaises(pyyoutube.PyYouTubeException):
            self.api.get_playlist_items(playlist_id="id", parts="id,not_part")

        # test paged
        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL, json=self.PLAYLIST_ITEM_PAGED_1)
            m.add("GET", self.BASE_URL, json=self.PLAYLIST_ITEM_PAGED_2)

            res_by_playlist = self.api.get_playlist_items(
                playlist_id="PLOU2XLYxmsIKpaV8h0AGE05so0fAwwfTw",
                parts="id,snippet",
                limit=10,
                count=20,
            )
            self.assertEqual(res_by_playlist.kind, "youtube#playlistItemListResponse")
            self.assertEqual(res_by_playlist.pageInfo.totalResults, 13)
            self.assertEqual(len(res_by_playlist.items), 13)
            self.assertEqual(
                res_by_playlist.items[0].id,
                "UExPVTJYTFl4bXNJS3BhVjhoMEFHRTA1c28wZkF3d2ZUdy41NkI0NEY2RDEwNTU3Q0M2",
            )

        # test count
        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL, json=self.PLAYLIST_ITEM_PAGED_1)

            res_by_playlist = self.api.get_playlist_items(
                playlist_id="PLOU2XLYxmsIKpaV8h0AGE05so0fAwwfTw",
                parts="id,snippet",
                limit=10,
                count=5,
            )
            self.assertEqual(res_by_playlist.kind, "youtube#playlistItemListResponse")
            self.assertEqual(res_by_playlist.pageInfo.totalResults, 13)
            self.assertEqual(len(res_by_playlist.items), 5)
            self.assertEqual(
                res_by_playlist.items[0].id,
                "UExPVTJYTFl4bXNJS3BhVjhoMEFHRTA1c28wZkF3d2ZUdy41NkI0NEY2RDEwNTU3Q0M2",
            )

        # test get all items
        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL, json=self.PLAYLIST_ITEM_PAGED_1)
            m.add("GET", self.BASE_URL, json=self.PLAYLIST_ITEM_PAGED_2)

            res_by_playlist = self.api.get_playlist_items(
                playlist_id="PLOU2XLYxmsIKpaV8h0AGE05so0fAwwfTw",
                parts="id,snippet",
                count=None,
            )
            self.assertEqual(res_by_playlist.pageInfo.totalResults, 13)
            self.assertEqual(len(res_by_playlist.items), 13)

        # test filter
        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL, json=self.PLAYLIST_ITEM_FILTER)

            res_by_filter = self.api.get_playlist_items(
                playlist_id="PLOU2XLYxmsIKpaV8h0AGE05so0fAwwfTw",
                parts=("id", "snippet"),
                video_id="VCv-KKIkLns",
                return_json=True,
            )

            self.assertEqual(res_by_filter["pageInfo"]["totalResults"], 1)
            self.assertEqual(
                res_by_filter["items"][0]["snippet"]["resourceId"]["videoId"],
                "VCv-KKIkLns",
            )

        # test use page token
        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL, json=self.PLAYLIST_ITEM_PAGED_2)

            res_by_playlist = self.api.get_playlist_items(
                playlist_id="PLOU2XLYxmsIKpaV8h0AGE05so0fAwwfTw",
                parts="id,snippet",
                page_token="CAoQAA",
                count=3,
            )
            self.assertEqual(len(res_by_playlist.items), 3)
