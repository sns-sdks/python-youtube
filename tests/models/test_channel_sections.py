import json
import unittest

import pyyoutube.models as models


class ChannelSectionModelTest(unittest.TestCase):
    base_path = "testdata/modeldata/channel_sections/"

    with open(f"{base_path}channel_section_info.json", "rb") as f:
        CHANNEL_SECTION_INFO = json.loads(f.read().decode("utf-8"))
    with open(f"{base_path}channel_section_response.json", "rb") as f:
        CHANNEL_SECTION_RESPONSE = json.loads(f.read().decode("utf-8"))

    def testChannelSection(self) -> None:
        m = models.ChannelSection.from_dict(self.CHANNEL_SECTION_INFO)

        self.assertEqual(m.id, "UC_x5XG1OV2P6uZZ5FSM9Ttw.e-Fk7vMPqLE")
        self.assertEqual(m.snippet.type, "multipleChannels")
        self.assertEqual(len(m.contentDetails.channels), 16)

    def testChannelSectionResponse(self) -> None:
        m = models.ChannelSectionResponse.from_dict(self.CHANNEL_SECTION_RESPONSE)

        self.assertEqual(m.kind, "youtube#channelSectionListResponse")
        self.assertEqual(len(m.items), 10)
