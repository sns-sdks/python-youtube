"""
    Tests for thumbnails.
"""
import io

from .base import BaseTestCase
from pyyoutube.media import Media


class TestThumbnailsResource(BaseTestCase):
    RESOURCE = "thumbnails"

    def test_set(self, authed_cli):
        video_id = "zxTVeyG1600"
        media = Media(fd=io.StringIO("jpeg content"), mimetype="image/jpeg")

        upload = authed_cli.thumbnails.set(
            video_id=video_id,
            media=media,
        )
        assert upload.resumable_progress == 0
