import io

import pytest
import responses

import pyyoutube.models as mds
from .base import BaseTestCase
from pyyoutube.error import PyYouTubeException
from pyyoutube.media import Media


class TestVideosResource(BaseTestCase):
    RESOURCE = "videos"

    def test_list(self, helpers, authed_cli, key_cli):
        with pytest.raises(PyYouTubeException):
            key_cli.videos.list()

        with responses.RequestsMock() as m:
            m.add(
                method="GET",
                url=self.url,
                json=self.load_json("videos/videos_info_multi.json", helpers),
            )

            res = key_cli.videos.list(
                video_id=["D-lhorsDlUQ", "ovdbrdCIP7U"], parts=["snippet"]
            )
            assert len(res.items) == 2

        with responses.RequestsMock() as m:
            m.add(
                method="GET",
                url=self.url,
                json=self.load_json("videos/videos_chart_paged_1.json", helpers),
            )

            res = key_cli.videos.list(chart="mostPopular", parts=["snippet"])
            assert len(res.items) == 5

        with responses.RequestsMock() as m:
            m.add(
                method="GET",
                url=self.url,
                json=self.load_json("videos/videos_myrating_paged_1.json", helpers),
            )

            res = key_cli.videos.list(my_rating="like", parts=["snippet"])
            assert len(res.items) == 2

    def test_insert(self, helpers, authed_cli):
        body = mds.Video(
            snippet=mds.VideoSnippet(
                title="video title",
                description="video description",
            )
        )
        media = Media(fd=io.StringIO("video content"), mimetype="video/mp4")

        upload = authed_cli.videos.insert(
            body=body,
            media=media,
            notify_subscribers=True,
        )
        assert upload.resumable_progress == 0

    def test_update(self, helpers, authed_cli):
        body = mds.Video(
            snippet=mds.VideoSnippet(
                title="updated video title",
            )
        )

        with responses.RequestsMock() as m:
            m.add(
                method="PUT",
                url=self.url,
                json=self.load_json("videos/insert_response.json", helpers),
            )
            video = authed_cli.videos.update(body=body, parts=["snippet"])
            assert video.id == "D-lhorsDlUQ"

    def test_rate(self, helpers, authed_cli):
        video_id = "D-lhorsDlUQ"

        with responses.RequestsMock() as m:
            m.add(method="POST", url=f"{self.url}/rate", status=204)

            assert authed_cli.videos.rate(
                video_id=video_id,
                rating="like",
            )

        with pytest.raises(PyYouTubeException):
            with responses.RequestsMock() as m:
                m.add(
                    method="POST",
                    url=f"{self.url}/rate",
                    status=403,
                    json=self.load_json("error_permission_resp.json", helpers),
                )
                authed_cli.videos.rate(
                    video_id=video_id,
                    rating="like",
                )

    def test_get_rating(self, helpers, authed_cli):
        video_id = "D-lhorsDlUQ"

        with responses.RequestsMock() as m:
            m.add(
                method="GET",
                url=f"{self.url}/getRating",
                json=self.load_json("videos/get_rating_response.json", helpers),
            )

            res = authed_cli.videos.get_rating(
                video_id=video_id,
            )
            assert res.items[0].rating == "none"

    def test_report_abuse(self, helpers, authed_cli):
        body = mds.VideoReportAbuse(
            videoId="D-lhorsDlUQ",
            reasonId="xxxxxx",
        )

        with responses.RequestsMock() as m:
            m.add(method="POST", url=f"{self.url}/reportAbuse", status=204)
            assert authed_cli.videos.report_abuse(body=body)

        with pytest.raises(PyYouTubeException):
            with responses.RequestsMock() as m:
                m.add(
                    method="POST",
                    url=f"{self.url}/reportAbuse",
                    status=403,
                    json=self.load_json("error_permission_resp.json", helpers),
                )
                authed_cli.videos.report_abuse(body=body)

    def test_delete(self, helpers, authed_cli):
        video_id = "D-lhorsDlUQ"

        with responses.RequestsMock() as m:
            m.add(method="DELETE", url=self.url, status=204)
            assert authed_cli.videos.delete(video_id=video_id)

        with pytest.raises(PyYouTubeException):
            with responses.RequestsMock() as m:
                m.add(
                    method="DELETE",
                    url=self.url,
                    status=403,
                    json=self.load_json("error_permission_resp.json", helpers),
                )
                authed_cli.videos.delete(video_id=video_id)
