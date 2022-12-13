"""
    Tests for media upload.
"""
import io

import pytest
import responses
from requests import Response

from pyyoutube.error import PyYouTubeException
from pyyoutube.media import Media, MediaUpload, MediaUploadProgress


class TestMedia:
    def test_initial(self, tmp_path):
        with pytest.raises(PyYouTubeException):
            Media()

        d = tmp_path / "sub"
        d.mkdir()
        f = d / "simple.vvv"
        f.write_bytes(b"asd")
        m = Media(filename=str(f))
        assert m.mimetype == "application/octet-stream"

        f1 = d / "video.mp4"
        f1.write_text("video")
        m = Media(fd=f1.open("rb"))
        assert m.size == 5
        assert m.get_bytes(0, 2)


class TestMediaUploadProgress:
    def test_progress(self):
        pg = MediaUploadProgress(10, 20)
        assert pg.progress() == 0.5
        assert str(pg)

        pg = MediaUploadProgress(10, 0)
        assert pg.progress() == 0.0


class TestMediaUpload:
    def test_upload(self, helpers, authed_cli):
        location = "https://youtube.googleapis.com/upload/youtube/v3/videos?part=snippet&alt=json&uploadType=resumable&upload_id=upload_id"

        media = Media(fd=io.StringIO("1234567890"), mimetype="video/mp4", chunk_size=5)
        upload = MediaUpload(
            client=authed_cli,
            resource="videos",
            media=media,
            params={"part": "snippet"},
            body={"body": '{"snippet": {dasd}}'},
        )

        with responses.RequestsMock() as m:
            m.add(
                method="POST",
                url="https://www.googleapis.com/upload/youtube/v3/videos",
                status=200,
                adding_headers={"location": location},
            )
            m.add(
                method="PUT",
                url=location,
                status=308,
                adding_headers={
                    "range": "0-4",
                },
            )
            m.add(
                method="PUT",
                url=location,
                json=helpers.load_json("testdata/apidata/videos/insert_response.json"),
            )

            pg, body = upload.next_chunk()
            assert pg.progress() == 0.5
            assert body is None

            pg, body = upload.next_chunk()
            assert pg is None
            assert body["id"] == "D-lhorsDlUQ"

    def test_upload_response(self, authed_cli, helpers):
        location = "https://youtube.googleapis.com/upload/youtube/v3/videos?part=snippet&alt=json&uploadType=resumable&upload_id=upload_id"
        media = Media(
            fd=io.StringIO("1234567890"),
            mimetype="video/mp4",
        )
        upload = MediaUpload(
            client=authed_cli,
            resource="videos",
            media=media,
            params={"part": "snippet"},
            body={"body": '{"snippet": {dasd}}'},
        )

        with pytest.raises(PyYouTubeException):
            with responses.RequestsMock() as m:
                m.add(
                    method="POST",
                    url="https://www.googleapis.com/upload/youtube/v3/videos",
                    status=400,
                    json=helpers.load_json("testdata/error_response.json"),
                )
                upload.next_chunk()

        with responses.RequestsMock() as m:
            m.add(
                method="PUT",
                url=location,
                status=308,
            )
            upload.resumable_uri = location
            upload.next_chunk()

        with pytest.raises(PyYouTubeException):
            with responses.RequestsMock() as m:
                m.add(
                    method="PUT",
                    url=location,
                    status=400,
                    json=helpers.load_json("testdata/error_response.json"),
                )
                upload.resumable_uri = location
                upload.next_chunk()

        resp = Response()
        resp.status_code = 308
        resp.headers = {"location": location}
        upload.process_response(resp=resp)
