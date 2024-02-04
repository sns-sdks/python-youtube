"""
    Media object to upload.
"""

import mimetypes
import os
from typing import IO, Optional, Tuple

from requests import Response

from pyyoutube.error import PyYouTubeException, ErrorMessage, ErrorCode

DEFAULT_CHUNK_SIZE = 20 * 1024 * 1024


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


class MediaUploadProgress:
    def __init__(self, progressed_seize: int, total_size: int):
        """
        Args:
            progressed_seize: Bytes sent so far.
            total_size: Total bytes in complete upload, or None if the total
            upload size isn't known ahead of time.
        """
        self.progressed_seize = progressed_seize
        self.total_size = total_size

    def progress(self) -> float:
        """Percent of upload completed, as a float.

        Returns:
          the percentage complete as a float, returning 0.0 if the total size of
          the upload is unknown.
        """
        if self.total_size is not None and self.total_size != 0:
            return float(self.progressed_seize) / float(self.total_size)
        else:
            return 0.0

    def __repr__(self) -> str:
        return f"Media upload {int(self.progress() * 100)} complete."


class MediaUpload:
    def __init__(
        self,
        client,
        resource: str,
        media: Media,
        params: Optional[dict] = None,
        body: Optional[dict] = None,
    ) -> None:
        """Constructor for upload a file.

        Args:
            client:
                Client instance.
            resource:
                Resource like videos,captions and so on.
            media:
                Media instance.
            params:
                Parameters for the request.
            body:
                Body for the request.
        """
        self.client = client
        self.media = media
        self.params = params
        self.body = body
        self.resource = resource

        if self.params is not None:
            self.params["uploadType"] = "resumable"

        self.resumable_uri = None  # Real uri to upload media.
        self.resumable_progress = 0  # The bytes that have been uploaded.

    def next_chunk(self) -> Tuple[Optional[MediaUploadProgress], Optional[dict]]:
        """Execute the next step of a resumable upload.

        Returns:
            The body will be None until the resumable media is fully uploaded.
        """
        size = str(self.media.size)

        if self.resumable_uri is None:
            start_headers = {
                "X-Upload-Content-Type": self.media.mimetype,
                "X-Upload-Content-Length": size,
                "content-length": str(len(str(self.body or ""))),
            }
            resp = self.client.request(
                method="POST",
                path=self.resource,
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
        # An empty file results in chunk_end = -1 and size = 0
        # sending "bytes 0--1/0" results in an invalid request
        # Only add header "Content-Range" if chunk_end != -1
        if chunk_end != -1:
            headers["Content-Range"] = (
                f"bytes {self.resumable_progress}-{chunk_end}/{size}"
            )

        resp = self.client.request(
            path=self.resumable_uri,
            method="PUT",
            data=data,
            headers=headers,
        )
        return self.process_response(resp)

    def process_response(
        self, resp: Response
    ) -> Tuple[Optional[MediaUploadProgress], Optional[dict]]:
        """Process the response from chunk upload.

        Args:
            resp: Response for request.

        Returns:
            The body will be None until the resumable media is fully uploaded.
        """
        if resp.status_code in [200, 201]:
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
