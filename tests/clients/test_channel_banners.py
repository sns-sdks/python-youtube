"""
    Tests for channel banners
"""
import io

from .base import BaseTestCase
from pyyoutube.media import Media


class TestChannelBanners(BaseTestCase):
    def test_insert(self, helpers, authed_cli):
        media = Media(fd=io.StringIO("jpg content"), mimetype="image/jpeg")
        upload = authed_cli.channelBanners.insert(media=media)

        assert upload.resumable_progress == 0
