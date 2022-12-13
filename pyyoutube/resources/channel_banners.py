"""
    Channel banners resource implementation.
"""
from typing import Optional

from pyyoutube.resources.base_resource import Resource
from pyyoutube.media import Media, MediaUpload


class ChannelBannersResource(Resource):
    """A channelBanner resource contains the URL that you would use to set a newly uploaded image as
    the banner image for a channel.

    References: https://developers.google.com/youtube/v3/docs/channelBanners
    """

    def insert(
        self,
        media: Media,
        on_behalf_of_content_owner: Optional[str] = None,
        **kwargs: Optional[dict],
    ) -> MediaUpload:
        """Uploads a channel banner image to YouTube.

        Args:
            media:
                Banner media data.
            on_behalf_of_content_owner:
                The onBehalfOfContentOwner parameter indicates that the request's authorization
                credentials identify a YouTube CMS user who is acting on behalf of the content
                owner specified in the parameter value. This parameter is intended for YouTube
                content partners that own and manage many different YouTube channels. It allows
                content owners to authenticate once and get access to all their video and channel
                data, without having to provide authentication credentials for each individual channel.
                The CMS account that the user authenticates with must be linked to the specified YouTube content owner.
            **kwargs:
                Additional parameters for system parameters.
                Refer: https://cloud.google.com/apis/docs/system-parameters.

        Returns:
            Channel banner data.
        """
        params = {"onBehalfOfContentOwner": on_behalf_of_content_owner, **kwargs}
        # Build a media upload instance.
        media_upload = MediaUpload(
            client=self._client,
            resource="channelBanners/insert",
            media=media,
            params=params,
        )
        return media_upload
