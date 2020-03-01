import json
import unittest

import pyyoutube.models as models


class CaptionModelTest(unittest.TestCase):
    BASE_PATH = "testdata/modeldata/captions/"

    with open(BASE_PATH + "caption_snippet.json", "rb") as f:
        CAPTION_SNIPPET = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "caption.json", "rb") as f:
        CAPTION_INFO = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "caption_response.json", "rb") as f:
        CAPTION_RESPONSE = json.loads(f.read().decode("utf-8"))

    def testCaptionSnippet(self):
        m = models.CaptionSnippet.from_dict(self.CAPTION_SNIPPET)

        self.assertEqual(m.videoId, "oHR3wURdJ94")
        self.assertEqual(
            m.string_to_datetime(m.lastUpdated).isoformat(),
            "2020-01-14T09:40:49.981000+00:00",
        )

    def testCaption(self):
        m = models.Caption.from_dict(self.CAPTION_INFO)

        self.assertEqual(m.id, "SwPOvp0r7kd9ttt_XhcHdZthMwXG7Z0I")
        self.assertEqual(m.snippet.videoId, "oHR3wURdJ94")

    def testCaptionListResponse(self):
        m = models.CaptionListResponse.from_dict(self.CAPTION_RESPONSE)

        self.assertEqual(m.kind, "youtube#captionListResponse")
        self.assertEqual(len(m.items), 2)
        self.assertEqual(m.items[0].id, "SwPOvp0r7kd9ttt_XhcHdZthMwXG7Z0I")
