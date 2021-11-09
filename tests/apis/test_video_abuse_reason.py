import json
import unittest
import aiohttp

import responses
import pyyoutube


class ApiVideoAbuseReason(unittest.IsolatedAsyncioTestCase):
    BASE_PATH = "testdata/apidata/abuse_reasons/"
    BASE_URL = "https://www.googleapis.com/youtube/v3/videoAbuseReportReasons"
    session = aiohttp.ClientSession()

    with open(BASE_PATH + "abuse_reason.json", "rb") as f:
        ABUSE_REASON_RES = json.loads(f.read().decode("utf-8"))

    def setUp(self) -> None:
        self.api_with_token = pyyoutube.Api(self.session, access_token="access token")

    async def testGetVideoAbuseReportReason(self) -> None:
        with responses.RequestsMock() as m:
            m.add("GET", self.BASE_URL, json=self.ABUSE_REASON_RES)

            abuse_res = await self.api_with_token.get_video_abuse_report_reason(
                parts=["id", "snippet"],
            )

            self.assertEqual(
                abuse_res.kind, "youtube#videoAbuseReportReasonListResponse"
            )
            self.assertEqual(len(abuse_res.items), 3)

            abuse_res_json = await self.api_with_token.get_video_abuse_report_reason(
                return_json=True
            )

            self.assertEqual(len(abuse_res_json["items"]), 3)
