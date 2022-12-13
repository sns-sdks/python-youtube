"""
    Thumbnails resources implementation.
"""
from typing import Optional

from pyyoutube.resources.base_resource import Resource
from pyyoutube.media import Media, MediaUpload


class ThumbnailsResource(Resource):
    """A thumbnail resource identifies different thumbnail image sizes associated with a resource.

    References: https://developers.google.com/youtube/v3/docs/thumbnails
    """

    def set(
        self,
        video_id: str,
        media: Media,
        on_behalf_of_content_owner: Optional[str] = None,
        **kwargs: Optional[dict],
    ) -> MediaUpload:
        params = {
            "videoId": video_id,
            "onBehalfOfContentOwner": on_behalf_of_content_owner,
            **kwargs,
        }
        # Build a media upload instance.
        media_upload = MediaUpload(
            client=self._client,
            resource="thumbnails/set",
            media=media,
            params=params,
        )
        return media_upload
