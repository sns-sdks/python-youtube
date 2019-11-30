import json
import unittest
import pyyoutube
import pyyoutube.models as models


class VideoModelTest(unittest.TestCase):
    BASE_PATH = "testdata/modeldata/videos/"

    with open(BASE_PATH + "video_content_details.json", "rb") as f:
        CONTENT_DETAILS_INFO = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "video_topic_details.json", "rb") as f:
        TOPIC_DETAILS_INFO = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "video_snippet.json", "rb") as f:
        SNIPPET_INFO = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "video_statistics.json", "rb") as f:
        STATISTICS_INFO = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "video_status.json", "rb") as f:
        STATUS_INFO = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "video_info.json", "rb") as f:
        VIDEO_INFO = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "video_api_response.json", "rb") as f:
        VIDEO_API_RESPONSE = json.loads(f.read().decode("utf-8"))

    def testVideoContentDetails(self) -> None:
        m = models.VideoContentDetails.from_dict(self.CONTENT_DETAILS_INFO)

        self.assertEqual(m.duration, "PT21M7S")

        seconds = m.get_video_seconds_duration()
        self.assertEqual(seconds, 1267)

        m.duration = None
        self.assertEqual(m.get_video_seconds_duration(), None)

        with self.assertRaises(pyyoutube.PyYouTubeException):
            m.duration = "error datetime"
            m.get_video_seconds_duration()

    def testVideoTopicDetails(self) -> None:
        m = models.VideoTopicDetails.from_dict(self.TOPIC_DETAILS_INFO)

        self.assertEqual(m.topicIds[0], "/m/02jjt")
        self.assertEqual(len(m.topicCategories), 1)

        full_topics = m.get_full_topics()

        self.assertEqual(full_topics[0].id, "/m/02jjt")
        self.assertEqual(full_topics[0].description, "Entertainment (parent topic)")

    def testVideoSnippet(self) -> None:
        m = models.VideoSnippet.from_dict(self.SNIPPET_INFO)

        self.assertEqual(
            m.string_to_datetime(m.publishedAt).isoformat(), "2019-03-21T20:37:49+00:00"
        )

        m.publishedAt = None
        self.assertEqual(m.string_to_datetime(m.publishedAt), None)

        with self.assertRaises(pyyoutube.PyYouTubeException):
            m.string_to_datetime("error datetime string")

        self.assertEqual(m.channelId, "UC_x5XG1OV2P6uZZ5FSM9Ttw")
        self.assertEqual(
            m.thumbnails.default.url, "https://i.ytimg.com/vi/D-lhorsDlUQ/default.jpg"
        )
        self.assertEqual(m.tags[0], "Google")
        self.assertEqual(
            m.localized.title, "What are Actions on Google (Assistant on Air)"
        )

    def testVideoStatistics(self) -> None:
        m = models.VideoStatistics.from_dict(self.STATISTICS_INFO)

        self.assertEqual(m.viewCount, "8087")

    def testVideoStatus(self) -> None:
        m = models.VideoStatus.from_dict(self.STATUS_INFO)

        self.assertEqual(m.uploadStatus, "processed")

        self.assertEqual(
            m.string_to_datetime(m.publishAt).isoformat(), "2019-03-21T20:37:49+00:00"
        )

    def testVideo(self) -> None:
        m = models.Video.from_dict(self.VIDEO_INFO)

        self.assertEqual(m.id, "D-lhorsDlUQ")
        self.assertEqual(
            m.snippet.title, "What are Actions on Google (Assistant on Air)"
        )

    def testVideoListResponse(self) -> None:
        m = models.VideoListResponse.from_dict(self.VIDEO_API_RESPONSE)
        self.assertEqual(m.kind, "youtube#videoListResponse")
        self.assertEqual(m.pageInfo.totalResults, 1)
        self.assertEqual(m.items[0].id, "D-lhorsDlUQ")
