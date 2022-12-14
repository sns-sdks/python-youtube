"""
    Watermarks resource implementation.
"""
from typing import Optional, Union

from pyyoutube.resources.base_resource import Resource
from pyyoutube.media import Media, MediaUpload
from pyyoutube.models import Watermark


class WatermarksResource(Resource):
    def set(
        self,
        channel_id: str,
        body: Union[dict, Watermark],
        media: Media,
        on_behalf_of_content_owner: Optional[str] = None,
        **kwargs: Optional[dict],
    ) -> MediaUpload:
        """

        Args:
            channel_id:
                Specifies the YouTube channel ID for which the watermark is being provided.
            body:
                Provide watermark data in the request body. You can give dataclass or just a dict with data.
            media:
                Media for watermark image.
            on_behalf_of_content_owner:
                The onBehalfOfContentOwner parameter indicates that the request's authorization
                credentials identify a YouTube CMS user who is acting on behalf of the content
                owner specified in the parameter value. This parameter is intended for YouTube
                content partners that own and manage many difference YouTube channels. It allows
                content owners to authenticate once and get access to all their video and channel
                data, without having to provide authentication credentials for each individual channel.
                The CMS account that the user authenticates with must be linked to the specified YouTube content owner.
            **kwargs:
                Additional parameters for system parameters.
                Refer: https://cloud.google.com/apis/docs/system-parameters.
        Returns:
            Watermark set status.
        """
        params = {
            "channel_id": channel_id,
            "onBehalfOfContentOwner": on_behalf_of_content_owner,
            **kwargs,
        }

        # Build a media upload instance.
        media_upload = MediaUpload(
            client=self._client,
            resource="watermarks/set",
            media=media,
            params=params,
            body=body.to_dict_ignore_none(),
        )
        return media_upload

    def unset(
        self,
        channel_id: str,
        on_behalf_of_content_owner: Optional[str] = None,
        **kwargs: Optional[dict],
    ) -> bool:
        """Deletes a channel's watermark image.

        Args:
            channel_id:
                Specifies the YouTube channel ID for which the watermark is being unset.
            on_behalf_of_content_owner:
                The onBehalfOfContentOwner parameter indicates that the request's authorization
                credentials identify a YouTube CMS user who is acting on behalf of the content
                owner specified in the parameter value. This parameter is intended for YouTube
                content partners that own and manage many difference YouTube channels. It allows
                content owners to authenticate once and get access to all their video and channel
                data, without having to provide authentication credentials for each individual channel.
                The CMS account that the user authenticates with must be linked to the specified YouTube content owner.
            **kwargs:
                Additional parameters for system parameters.
                Refer: https://cloud.google.com/apis/docs/system-parameters.

        Returns:
            watermark unset status.
        """
        params = {
            "channelId": channel_id,
            "onBehalfOfContentOwner": on_behalf_of_content_owner,
            **kwargs,
        }
        response = self._client.request(
            method="POST",
            path="watermarks/unset",
            params=params,
        )
        if response.ok:
            return True
        self._client.parse_response(response=response)
