import responses

from .base import BaseTestCase


class TestVideoAbuseReportReasonsResource(BaseTestCase):
    RESOURCE = "videoAbuseReportReasons"

    def test_list(self, helpers, authed_cli):
        with responses.RequestsMock() as m:
            m.add(
                method="GET",
                url=self.url,
                json=self.load_json("abuse_reasons/abuse_reason.json", helpers),
            )

            res = authed_cli.videoAbuseReportReasons.list(
                parts=["id", "snippet"],
            )
            assert res.items[0].id == "N"
