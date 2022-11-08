"""
    Channel banners resource implementation.
"""
from typing import Optional, Union

from pyyoutube.resources.base_resource import Resource
from pyyoutube.models import ChannelBanner


class ChannelBannersResource(Resource):
    """A channelBanner resource contains the URL that you would use to set a newly uploaded image as
    the banner image for a channel.

    References: https://developers.google.com/youtube/v3/docs/channelBanners
    """

    # TODO upload file
    def insert(
        self,
        on_behalf_of_content_owner: Optional[str] = None,
        return_json: bool = False,
        **kwargs: Optional[dict],
    ) -> Union[dict, ChannelBanner]:
        """Uploads a channel banner image to YouTube.

        Args:
            on_behalf_of_content_owner:
            The onBehalfOfContentOwner parameter indicates that the request's authorization
                credentials identify a YouTube CMS user who is acting on behalf of the content
                owner specified in the parameter value. This parameter is intended for YouTube
                content partners that own and manage many different YouTube channels. It allows
                content owners to authenticate once and get access to all their video and channel
                data, without having to provide authentication credentials for each individual channel.
                The CMS account that the user authenticates with must be linked to the specified YouTube content owner.
            return_json:
                Type for returned data. If you set True JSON data will be returned.
            **kwargs:
                Additional parameters for system parameters.
                Refer: https://cloud.google.com/apis/docs/system-parameters.

        Returns:
            Channel banner data.
        """
        params = {"onBehalfOfContentOwner": on_behalf_of_content_owner, **kwargs}
        response = self._client.request(path="channelBanners", params=params)
        data = self._client.parse_response(response=response)
        return data if return_json else ChannelBanner.from_dict(data)
