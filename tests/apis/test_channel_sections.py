import json
import unittest

import aiohttp

import pyyoutube
import responses


class ApiChannelSectionTest(unittest.IsolatedAsyncioTestCase):
    BASE_PATH = "testdata/apidata/channel_sections/"
    BASE_URL = "https://www.googleapis.com/youtube/v3/channelSections"
    session = aiohttp.ClientSession()

    with open(BASE_PATH + "channel_sections_by_id.json", "rb") as f:
        CHANNEL_SECTIONS_BY_ID = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "channel_sections_by_ids.json", "rb") as f:
        CHANNEL_SECTIONS_BY_IDS = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "channel_sections_by_channel.json", "rb") as f:
        CHANNEL_SECTIONS_BY_CHANNEL = json.loads(f.read().decode("utf-8"))

    def setUp(self) -> None:
        self.api = pyyoutube.Api(self.session, api_key="api key")

    async def testGetChannelSectionsById(self) -> None:
        section_id = "UCa-vrCLQHviTOVnEKDOdetQ.nGzAI5pLbMY"
        section_ids = [
            "UC_x5XG1OV2P6uZZ5FSM9Ttw.npYvuMz0_es",
            "UC_x5XG1OV2P6uZZ5FSM9Ttw.9_wU0qhEPR8",
        ]

        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL, json=self.CHANNEL_SECTIONS_BY_ID)
            m.add("GET", self.BASE_URL, json=self.CHANNEL_SECTIONS_BY_IDS)

            section_res = await self.api.get_channel_sections_by_id(
                section_id=section_id,
            )
            self.assertEqual(section_res.kind, "youtube#channelSectionListResponse")
            self.assertEqual(len(section_res.items), 1)
            self.assertEqual(section_res.items[0].id, section_id)

            section_multi_res = await self.api.get_channel_sections_by_id(
                section_id=section_ids, parts=["id", "snippet"], return_json=True
            )

            self.assertEqual(len(section_multi_res["items"]), 2)
            self.assertIn(section_multi_res["items"][1]["id"], section_ids)

    async def testGetChannelSectionsByChannel(self) -> None:
        channel_id = "UCa-vrCLQHviTOVnEKDOdetQ"

        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL, json=self.CHANNEL_SECTIONS_BY_CHANNEL)

            section_by_channel = await self.api.get_channel_sections_by_channel(
                channel_id=channel_id,
            )

            self.assertEqual(len(section_by_channel.items), 3)
            self.assertEqual(
                section_by_channel.items[0].id, "UCa-vrCLQHviTOVnEKDOdetQ.jNQXAC9IVRw"
            )

            section_by_me = await self.api.get_channel_sections_by_channel(
                mine=True,
                return_json=True,
            )

            self.assertEqual(
                section_by_me["items"][2]["id"], "UCa-vrCLQHviTOVnEKDOdetQ.nGzAI5pLbMY"
            )
