import json
import unittest

import pyyoutube.models as models


class ActivityModelTest(unittest.TestCase):
    BASE_PATH = "testdata/modeldata/activities/"

    with open(BASE_PATH + "activity_contentDetails.json", "rb") as f:
        ACTIVITY_CONTENT_DETAILS = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "activity_snippet.json", "rb") as f:
        ACTIVITY_SNIPPET = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "activity.json", "rb") as f:
        ACTIVITY = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "activity_response.json", "rb") as f:
        ACTIVITY_RESPONSE = json.loads(f.read().decode("utf-8"))

    def testActivityContentDetails(self) -> None:
        m = models.ActivityContentDetails.from_dict(self.ACTIVITY_CONTENT_DETAILS)

        self.assertEqual(m.upload.videoId, "LDXYRzerjzU")

    def testActivitySnippet(self) -> None:
        m = models.ActivitySnippet.from_dict(self.ACTIVITY_SNIPPET)

        self.assertEqual(m.channelId, "UC_x5XG1OV2P6uZZ5FSM9Ttw")
        self.assertEqual(
            m.thumbnails.default.url, "https://i.ytimg.com/vi/DQGSZTxLVrI/default.jpg"
        )

    def testActivity(self) -> None:
        m = models.Activity.from_dict(self.ACTIVITY)

        self.assertEqual(m.snippet.channelId, "UCa-vrCLQHviTOVnEKDOdetQ")
        self.assertEqual(m.contentDetails.upload.videoId, "JE8xdDp5B8Q")

    def testActivityListResponse(self) -> None:
        m = models.ActivityListResponse.from_dict(self.ACTIVITY_RESPONSE)

        self.assertEqual(m.kind, "youtube#activityListResponse")
        self.assertEqual(m.pageInfo.totalResults, 2)
        self.assertEqual(len(m.items), 2)
