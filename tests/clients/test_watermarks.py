"""
    Tests for watermarks.
"""

import io

import pytest
import responses

import pyyoutube.models as mds
from .base import BaseTestCase
from pyyoutube.error import PyYouTubeException
from pyyoutube.media import Media


class TestWatermarksResource(BaseTestCase):
    RESOURCE = "watermarks"

    def test_set(self, authed_cli):
        body = mds.Watermark(
            timing=mds.WatermarkTiming(
                type="offsetFromStart",
                offsetMs=1000,
                durationMs=3000,
            ),
            position=mds.WatermarkPosition(
                type="corner",
                cornerPosition="topRight",
            ),
        )
        media = Media(fd=io.StringIO("image content"), mimetype="image/jpeg")

        upload = authed_cli.watermarks.set(
            channel_id="id",
            body=body,
            media=media,
        )
        assert upload.resumable_progress == 0

    def test_unset(self, helpers, authed_cli):
        with responses.RequestsMock() as m:
            m.add(method="POST", url=f"{self.url}/unset", status=204)
            assert authed_cli.watermarks.unset(channel_id="id")

        with pytest.raises(PyYouTubeException):
            with responses.RequestsMock() as m:
                m.add(
                    method="POST",
                    url=f"{self.url}/unset",
                    status=403,
                    json=self.load_json("error_permission_resp.json", helpers),
                )
                assert authed_cli.watermarks.unset(channel_id="id")
