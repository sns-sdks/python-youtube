import json
import unittest

import responses

import pyyoutube


class ApiPlaylistTest(unittest.TestCase):
    BASE_PATH = "testdata/apidata/playlists/"
    BASE_URL = "https://www.googleapis.com/youtube/v3/playlists"

    with open(BASE_PATH + "playlists_single.json", "rb") as f:
        PLAYLISTS_INFO_SINGLE = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "playlists_multi.json", "rb") as f:
        PLAYLISTS_INFO_MULTI = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "playlists_paged_1.json", "rb") as f:
        PLAYLISTS_PAGED_1 = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "playlists_paged_2.json", "rb") as f:
        PLAYLISTS_PAGED_2 = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "playlists_mine.json", "rb") as f:
        PLAYLISTS_MINE = json.loads(f.read().decode("utf-8"))

    def setUp(self) -> None:
        self.api = pyyoutube.Api(api_key="api key")
        self.api_with_access_token = pyyoutube.Api(access_token="access token")

    def testGetPlaylistById(self) -> None:
        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL, json=self.PLAYLISTS_INFO_SINGLE)
            m.add("GET", self.BASE_URL, json=self.PLAYLISTS_INFO_MULTI)

            res_by_playlist_id = self.api.get_playlist_by_id(
                playlist_id="PLOU2XLYxmsIJXsH2htG1g0NUjHGq62Q7i",
                parts="id,snippet",
                return_json=True,
            )
            self.assertEqual(res_by_playlist_id["kind"], "youtube#playlistListResponse")
            self.assertEqual(
                res_by_playlist_id["items"][0]["id"],
                "PLOU2XLYxmsIJXsH2htG1g0NUjHGq62Q7i",
            )

            res_by_playlist_multi_id = self.api.get_playlist_by_id(
                playlist_id=[
                    "PLOU2XLYxmsIJXsH2htG1g0NUjHGq62Q7i",
                    "PLOU2XLYxmsIJJVnHWmd1qfr0Caq4VZCu4",
                ],
                parts=["id", "snippet"],
            )
            self.assertEqual(len(res_by_playlist_multi_id.items), 2)
            self.assertEqual(
                res_by_playlist_multi_id.items[1].id,
                "PLOU2XLYxmsIJJVnHWmd1qfr0Caq4VZCu4",
            )

    def testGetPlaylists(self) -> None:
        # test params checker
        with self.assertRaises(pyyoutube.PyYouTubeException):
            self.api.get_playlists(parts="id,not_part")
        with self.assertRaises(pyyoutube.PyYouTubeException):
            self.api.get_playlists()

        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL, json=self.PLAYLISTS_PAGED_1)
            m.add("GET", self.BASE_URL, json=self.PLAYLISTS_PAGED_2)
            m.add("GET", self.BASE_URL, json=self.PLAYLISTS_MINE)

            res_by_channel_id = self.api.get_playlists(
                channel_id="UC_x5XG1OV2P6uZZ5FSM9Ttw",
                limit=10,
                count=13,
            )
            self.assertEqual(res_by_channel_id.pageInfo.totalResults, 422)
            self.assertEqual(len(res_by_channel_id.items), 13)
            self.assertEqual(
                res_by_channel_id.items[0].snippet.channelId, "UC_x5XG1OV2P6uZZ5FSM9Ttw"
            )

            res_by_mine = self.api_with_access_token.get_playlists(
                mine=True, limit=10, count=10, return_json=True
            )
            self.assertEqual(len(res_by_mine["items"]), 2)
            self.assertEqual(
                res_by_mine["items"][0]["id"], "PLOU2XLYxmsIIOSO0eWuj-6yQmdakarUzN"
            )

        # test for all items
        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL, json=self.PLAYLISTS_PAGED_1)
            m.add("GET", self.BASE_URL, json=self.PLAYLISTS_PAGED_2)

            res_by_channel_id = self.api.get_playlists(
                channel_id="UC_x5XG1OV2P6uZZ5FSM9Ttw",
                count=None,
            )
            self.assertEqual(len(res_by_channel_id.items), 20)

        # test for page token
        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL, json=self.PLAYLISTS_PAGED_2)

            res_by_channel_id = self.api.get_playlists(
                channel_id="UC_x5XG1OV2P6uZZ5FSM9Ttw", count=None, page_token="CAoQAA"
            )
            self.assertEqual(len(res_by_channel_id.items), 10)
