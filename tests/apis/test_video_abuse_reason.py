import json
import unittest

import responses
import pyyoutube


class ApiVideoAbuseReason(unittest.TestCase):
    BASE_PATH = "testdata/apidata/abuse_reasons/"
    BASE_URL = "https://www.googleapis.com/youtube/v3/videoAbuseReportReasons"

    with open(BASE_PATH + "abuse_reason.json", "rb") as f:
        ABUSE_REASON_RES = json.loads(f.read().decode("utf-8"))

    def setUp(self) -> None:
        self.api_with_token = pyyoutube.Api(access_token="access token")

    def testGetVideoAbuseReportReason(self) -> None:
        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL, json=self.ABUSE_REASON_RES)

            abuse_res = self.api_with_token.get_video_abuse_report_reason(
                parts=["id", "snippet"],
            )

            self.assertEqual(
                abuse_res.kind, "youtube#videoAbuseReportReasonListResponse"
            )
            self.assertEqual(len(abuse_res.items), 3)

            abuse_res_json = self.api_with_token.get_video_abuse_report_reason(
                return_json=True
            )

            self.assertEqual(len(abuse_res_json["items"]), 3)
