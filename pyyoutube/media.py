"""
    Media object to upload.
"""
import mimetypes
import os
from typing import Optional, IO

from requests import Response

from pyyoutube.error import PyYouTubeException, ErrorMessage, ErrorCode

DEFAULT_CHUNK_SIZE = 100 * 1024 * 1024


class Media:
    def __init__(
        self,
        fd: Optional[IO] = None,
        mimetype: Optional[str] = None,
        filename: Optional[str] = None,
        chunk_size: int = DEFAULT_CHUNK_SIZE,
    ) -> None:
        """Media representing a file to upload with metadata.

        Args:
            fd:
                The source of the bytes to upload.
            mimetype:
                Mime-type of the file.
            filename:
                Name of the file.
                At least one of the `fd` or `filename`.
            chunk_size:
                File will be uploaded in chunks of this many bytes. Only
                used if resumable=True.
        """

        if fd is not None:
            self.fd = fd
        elif filename is not None:
            self._filename = filename
            self.fd = open(self._filename, "rb")
        else:
            raise PyYouTubeException(
                ErrorMessage(
                    status_code=ErrorCode.MISSING_PARAMS,
                    message="Specify at least one of fd or filename",
                )
            )

        if mimetype is None and filename is not None:
            mimetype, _ = mimetypes.guess_type(filename)
            if mimetype is None:
                # Guess failed, use octet-stream.
                mimetype = "application/octet-stream"
        self.mimetype = mimetype
        self.chunk_size = chunk_size

        self.fd.seek(0, os.SEEK_END)
        self.size = self.fd.tell()

    def get_bytes(self, begin: int, length: int) -> bytes:
        """Get bytes from the media.

        Args:
          begin:
            Offset from beginning of file.
          length:
            Number of bytes to read, starting at begin.

        Returns:
          A string of bytes read. May be shorted than length if EOF was reached
          first.
        """
        self.fd.seek(begin)
        return self.fd.read(length)

    @classmethod
    def new_from_json(cls, data: dict):
        return Media(**data)


class MediaUpload:
    def __init__(
        self,
        client,
        media: Media,
        params: Optional[dict] = None,
        body: Optional[dict] = None,
    ):
        """
        Instance to upload a file.
        Args:
            client: Client instance.
            media: Media instance.
            params: Parameters for the request.
            body: Body for the request.
        """
        self.client = client
        self.media = media
        self.params = params
        self.body = body

        if self.params is not None:
            self.params["uploadType"] = "resumable"

        self.resumable_uri = None  # Real uri to upload media.
        self.resumable_progress = 0  # The bytes that have been uploaded.

    def next_chunk(self):
        if self.media.size is None:
            size = "*"
        else:
            size = str(self.media.size)

        # 1231244
        if self.resumable_uri is None:
            start_headers = {
                "X-Upload-Content-Type": self.media.mimetype,
                "X-Upload-Content-Length": size,
                "content-length": str(len(str(self.body or ""))),
            }
            resp = self.client.request(
                method="POST",
                path="videos",
                params=self.params,
                json=self.body,
                is_upload=True,
                headers=start_headers,
            )
            if resp.status_code == 200 and "location" in resp.headers:
                self.resumable_uri = resp.headers["location"]
            else:
                raise PyYouTubeException(resp)

        data = self.media.get_bytes(self.resumable_progress, self.media.chunk_size)

        # A short read implies that we are at EOF, so finish the upload.
        if len(data) < self.media.chunk_size:
            size = str(self.resumable_progress + len(data))

        chunk_end = self.resumable_progress + len(data) - 1

        headers = {
            "Content-Length": str(chunk_end - self.resumable_progress + 1),
        }
        if chunk_end != -1:
            headers[
                "Content-Range"
            ] = f"bytes {self.resumable_progress}-{chunk_end}/{size}"

        resp = self.client.request(
            path=self.resumable_uri,
            method="PUT",
            data=data,
            headers=headers,
        )
        return self.process_response(resp)

    def process_response(self, resp: Response):
        """
        Args:
            resp: Response for request.

        Returns:
            (UploadProgress, response body)
        """
        if resp.ok:
            return None, self.client.parse_response(response=resp)
        elif resp.status_code == 308:
            try:
                self.resumable_progress = int(resp.headers["range"].split("-")[1]) + 1
            except KeyError:
                # If resp doesn't contain range header, resumable progress is 0
                self.resumable_progress = 0
            if "location" in resp.headers:
                self.resumable_uri = resp.headers["location"]
        else:
            raise PyYouTubeException(resp)

        return (
            MediaUploadProgress(self.resumable_progress, self.media.size),
            None,
        )


class MediaUploadProgress:
    def __init__(self, progressed_seize, total_size):
        self.progressed_seize = progressed_seize
        self.total_size = total_size

    def progress(self):
        if self.total_size is not None and self.total_size != 0:
            return float(self.progressed_seize) / float(self.total_size)
        else:
            return 0.0
