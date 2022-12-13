"""
    Tests for captions resources.
"""
import io

import pytest
import responses

import pyyoutube.models as mds
from .base import BaseTestCase
from pyyoutube.error import PyYouTubeException
from pyyoutube.media import Media


class TestCaptionsResource(BaseTestCase):
    RESOURCE = "captions"

    def test_list(self, helpers, key_cli):
        with responses.RequestsMock() as m:
            m.add(
                method="GET",
                url=self.url,
                json=self.load_json("captions/captions_by_video.json", helpers),
            )

            res = key_cli.captions.list(parts=["snippet"], video_id="oHR3wURdJ94")
            assert res.items[0].id == "SwPOvp0r7kd9ttt_XhcHdZthMwXG7Z0I"

    def test_insert(self, helpers, authed_cli):
        video_id = "zxTVeyG1600"

        body = mds.Caption(
            snippet=mds.CaptionSnippet(
                name="日文字幕", language="ja", videoId=video_id, isDraft=True
            )
        )
        media = Media(
            io.StringIO(
                """
        1
        00:00:00,036 --> 00:00:00,703
        ジメジメした天気
        """
            )
        )

        upload = authed_cli.captions.insert(
            body=body,
            media=media,
        )
        assert upload.resumable_progress == 0

    def test_update(self, helpers, authed_cli):
        caption_id = "AUieDabWmL88_xoRtxyxjTMtmvdoF9dLTW3WxfJvaThUXkNptljUijDFS-kDjyA"

        new_body = mds.Caption(
            id=caption_id,
            snippet=mds.CaptionSnippet(videoId="zxTVeyG1600", isDraft=False),
        )
        media = Media(
            io.StringIO(
                """
                1
                00:00:00,036 --> 00:00:00,703
                ジメジメした天気
                """
            ),
        )

        upload = authed_cli.captions.update(
            body=new_body,
            media=media,
        )
        assert upload.resumable_progress == 0

        with responses.RequestsMock() as m:
            m.add(
                method="PUT",
                url=self.url,
                json=self.load_json("captions/update_response.json", helpers),
            )

            caption = authed_cli.captions.update(body=new_body)
            assert not caption.snippet.isDraft

    def test_download(self, authed_cli):
        caption_id = "AUieDabWmL88_xoRtxyxjTMtmvdoF9dLTW3WxfJvaThUXkNptljUijDFS-kDjyA"

        with responses.RequestsMock() as m:
            m.add(
                method="GET",
                url=f"{self.url}/{caption_id}",
            )
            res = authed_cli.captions.download(caption_id=caption_id)
            assert res.status_code == 200

    def test_delete(self, helpers, authed_cli):
        caption_id = "AUieDabWmL88_xoRtxyxjTMtmvdoF9dLTW3WxfJvaThUXkNptljUijDFS-kDjyA"

        with responses.RequestsMock() as m:
            m.add(method="DELETE", url=self.url)
            assert authed_cli.captions.delete(caption_id=caption_id)

        with pytest.raises(PyYouTubeException):
            with responses.RequestsMock() as m:
                m.add(
                    method="DELETE",
                    url=self.url,
                    status=403,
                    json=self.load_json("error_permission_resp.json", helpers),
                )
                authed_cli.captions.delete(caption_id=caption_id)
