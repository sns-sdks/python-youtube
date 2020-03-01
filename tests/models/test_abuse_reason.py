import json
import unittest

import pyyoutube.models as models


class AbuseReasonModelTest(unittest.TestCase):
    BASE_PATH = "testdata/modeldata/abuse_report_reason/"

    with open(BASE_PATH + "abuse_reason.json", "rb") as f:
        ABUSE_REASON = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "abuse_reason_res.json", "rb") as f:
        ABUSE_REASON_RES = json.loads(f.read().decode("utf-8"))

    def testAbuseReason(self) -> None:
        m = models.VideoAbuseReportReason.from_dict(self.ABUSE_REASON)

        self.assertEqual(m.id, "N")
        self.assertEqual(m.snippet.label, "Sex or nudity")
        self.assertEqual(len(m.snippet.secondaryReasons), 3)

    def testAbuseReasonResponse(self) -> None:
        m = models.VideoAbuseReportReasonListResponse.from_dict(self.ABUSE_REASON_RES)

        self.assertEqual(m.kind, "youtube#videoAbuseReportReasonListResponse")
        self.assertEqual(len(m.items), 3)
