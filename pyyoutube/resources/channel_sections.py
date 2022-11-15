"""
    Channel Section resource implementation.
"""

from typing import Optional, Union

from pyyoutube.error import PyYouTubeException, ErrorMessage, ErrorCode
from pyyoutube.resources.base_resource import Resource
from pyyoutube.models import ChannelSection, ChannelSectionListResponse
from pyyoutube.utils.params_checker import enf_comma_separated, enf_parts


class ChannelSectionsResource(Resource):
    """A channelSection resource contains information about a set of videos that a channel has chosen to feature.

    References: https://developers.google.com/youtube/v3/docs/channelSections
    """

    def list(
        self,
        parts: Optional[Union[str, list, tuple, set]] = None,
        channel_id: Optional[str] = None,
        section_id: Optional[Union[str, list, tuple, set]] = None,
        mine: Optional[bool] = None,
        hl: Optional[str] = None,
        on_behalf_of_content_owner: Optional[str] = None,
        return_json: bool = False,
        **kwargs: Optional[dict],
    ) -> Union[dict, ChannelSectionListResponse]:
        """Returns a list of channelSection resources that match the API request criteria.

        Args:
            parts:
                Comma-separated list of one or more channel resource properties.
            channel_id:
                ID for the channel which you want to retrieve sections.
            section_id:
                Specifies a comma-separated list of IDs that uniquely identify the channelSection
                resources that are being retrieved.
            mine:
                Set this parameter's value to true to retrieve a feed of the channel sections
                associated with the authenticated user's YouTube channel.
            hl:
                The hl parameter provided support for retrieving localized metadata for a channel section.
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
            Channel section data.

        Raises:
            PyYouTubeException: Missing filter parameter.

        """
        params = {
            "part": enf_parts(resource="channelSections", value=parts),
            "hl": hl,
            "onBehalfOfContentOwner": on_behalf_of_content_owner,
            **kwargs,
        }
        if channel_id is not None:
            params["channelId"] = channel_id
        elif section_id is not None:
            params["id"] = enf_comma_separated(field="section_id", value=section_id)
        elif mine is not None:
            params["mine"] = mine
        else:
            raise PyYouTubeException(
                ErrorMessage(
                    status_code=ErrorCode.MISSING_PARAMS,
                    message=f"Specify at least one of for_username, id, managedByMe or mine",
                )
            )
        response = self._client.request(path="channelSections", params=params)
        data = self._client.parse_response(response=response)
        return data if return_json else ChannelSectionListResponse.from_dict(data)

    def insert(
        self,
        body: Union[dict, ChannelSection],
        parts: Optional[Union[str, list, tuple, set]] = None,
        on_behalf_of_content_owner: Optional[str] = None,
        on_behalf_of_content_owner_channel: Optional[str] = None,
        return_json: bool = False,
        **kwargs,
    ) -> Union[dict, ChannelSection]:
        """Adds a channel section to the authenticated user's channel.
        A channel can create a maximum of 10 shelves.

        Args:
            parts:
                The part parameter serves two purposes in this operation. It identifies the properties
                that the write operation will set as well as the properties that the API response will include.
                Accept values:
                    - id
                    - contentDetails
                    - snippet
            body:
                Provide a channelSection resource in the request body. You can give dataclass or just a dict with data.
            on_behalf_of_content_owner:
                The onBehalfOfContentOwner parameter indicates that the request's authorization
                credentials identify a YouTube CMS user who is acting on behalf of the content
                owner specified in the parameter value. This parameter is intended for YouTube
                content partners that own and manage many different YouTube channels. It allows
                content owners to authenticate once and get access to all their video and channel
                data, without having to provide authentication credentials for each individual channel.
                The CMS account that the user authenticates with must be linked to the specified YouTube content owner.
            on_behalf_of_content_owner_channel:
                The onBehalfOfContentOwnerChannel parameter specifies the YouTube channel ID of the
                channel to which a video is being added. This parameter is required when a request
                specifies a value for the onBehalfOfContentOwner parameter, and it can only be used
                in conjunction with that parameter. In addition, the request must be authorized
                using a CMS account that is linked to the content owner that the onBehalfOfContentOwner
                parameter specifies. Finally, the channel that the onBehalfOfContentOwnerChannel parameter
                value specifies must be linked to the content owner that the onBehalfOfContentOwner parameter specifies.
            return_json:
                Type for returned data. If you set True JSON data will be returned.
            **kwargs:
                Additional parameters for system parameters.
                Refer: https://cloud.google.com/apis/docs/system-parameters.

        Returns:
            Channel section data.
        """
        params = {
            "part": enf_parts(resource="channelSections", value=parts),
            "onBehalfOfContentOwner": on_behalf_of_content_owner,
            "onBehalfOfContentOwnerChannel": on_behalf_of_content_owner_channel,
            **kwargs,
        }
        response = self._client.request(
            method="POST",
            path="channelSections",
            params=params,
            json=body,
        )
        data = self._client.parse_response(response=response)
        return data if return_json else ChannelSection.from_dict(data)

    def update(
        self,
        body: Union[dict, ChannelSection],
        parts: Optional[Union[str, list, tuple, set]] = None,
        on_behalf_of_content_owner: Optional[str] = None,
        return_json: bool = False,
        **kwargs,
    ) -> Union[dict, ChannelSection]:
        """Updates a channel section.

        Args:
            parts:
                The part parameter serves two purposes in this operation. It identifies the properties
                that the write operation will set as well as the properties that the API response will include.
                Accept values:
                    - id
                    - contentDetails
                    - snippet
            body:
                Provide a channelSection resource in the request body. You can give dataclass or just a dict with data.
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
            Channel section data.
        """
        params = {
            "part": enf_parts(resource="channelSections", value=parts),
            "onBehalfOfContentOwner": on_behalf_of_content_owner,
            **kwargs,
        }
        response = self._client.request(
            method="PUT",
            path="channelSections",
            params=params,
            json=body,
        )
        data = self._client.parse_response(response=response)
        return data if return_json else ChannelSection.from_dict(data)

    def delete(
        self,
        section_id: str,
        on_behalf_of_content_owner: Optional[str] = None,
        **kwargs,
    ) -> bool:
        """Deletes a channel section.

        Args:
            section_id:
                ID for the target channel section.
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
            Channel section delete status
        """
        params = {
            "id": section_id,
            "onBehalfOfContentOwner": on_behalf_of_content_owner,
            **kwargs,
        }
        response = self._client.request(
            method="DELETE",
            path="channelSections",
            params=params,
        )
        if response.ok:
            return True
        self._client.parse_response(response=response)
