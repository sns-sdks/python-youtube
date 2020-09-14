import json
import unittest
import pyyoutube.models as models


class ChannelModelTest(unittest.TestCase):
    BASE_PATH = "testdata/modeldata/channels/"

    with open(BASE_PATH + "channel_branding_settings.json", "rb") as f:
        BRANDING_SETTINGS_INFO = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "channel_content_details.json", "rb") as f:
        CONTENT_DETAILS_INFO = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "channel_topic_details.json", "rb") as f:
        TOPIC_DETAILS_INFO = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "channel_snippet.json", "rb") as f:
        SNIPPET_INFO = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "channel_statistics.json", "rb") as f:
        STATISTICS_INFO = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "channel_status.json", "rb") as f:
        STATUS_INFO = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "channel_info.json", "rb") as f:
        CHANNEL_INFO = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "channel_api_response.json", "rb") as f:
        CHANNEL_API_RESPONSE = json.loads(f.read().decode("utf-8"))

    def testChannelBrandingSettings(self) -> None:
        m = models.ChannelBrandingSetting.from_dict(self.BRANDING_SETTINGS_INFO)

        self.assertEqual(m.channel.title, "Google Developers")

    def testChannelContentDetails(self) -> None:
        m = models.ChannelContentDetails.from_dict(self.CONTENT_DETAILS_INFO)

        self.assertEqual(m.relatedPlaylists.uploads, "UU_x5XG1OV2P6uZZ5FSM9Ttw")

    def testChannelTopicDetails(self) -> None:
        m = models.ChannelTopicDetails.from_dict(self.TOPIC_DETAILS_INFO)

        self.assertEqual(m.topicIds[0], "/m/019_rr")
        self.assertEqual(len(m.topicCategories), 3)

        full_topics = m.get_full_topics()
        self.assertEqual(full_topics[0].id, "/m/019_rr")
        self.assertEqual(full_topics[0].description, "Lifestyle (parent topic)")

    def testChannelSnippet(self) -> None:
        m = models.ChannelSnippet.from_dict(self.SNIPPET_INFO)

        self.assertEqual(m.title, "Google Developers")
        self.assertEqual(m.localized.title, "Google Developers")
        self.assertEqual(
            m.thumbnails.default.url,
            "https://yt3.ggpht.com/a/AGF-l78iFtAxyRZcUBzG91kbKMES19z-zGW5KT20_g=s88-c-k-c0xffffffff-no-rj-mo",
        )

        published_at = m.string_to_datetime(m.publishedAt)
        self.assertEqual(published_at.isoformat(), "2007-08-23T00:34:43+00:00")

    def testChannelStatistics(self) -> None:
        m = models.ChannelStatistics.from_dict(self.STATISTICS_INFO)

        self.assertEqual(m.viewCount, "160361638")

    def testChannelStatus(self) -> None:
        m = models.ChannelStatus.from_dict(self.STATUS_INFO)

        self.assertEqual(m.privacyStatus, "public")

    def testChannel(self) -> None:
        m = models.Channel.from_dict(self.CHANNEL_INFO)

        self.assertEqual(m.id, "UC_x5XG1OV2P6uZZ5FSM9Ttw")

    def testChannelListResponse(self) -> None:
        m = models.ChannelListResponse.from_dict(self.CHANNEL_API_RESPONSE)

        self.assertEqual(m.kind, "youtube#channelListResponse")
        self.assertEqual(m.pageInfo.totalResults, 1)
        self.assertEqual(m.items[0].id, "UC_x5XG1OV2P6uZZ5FSM9Ttw")
