"""
    Channel resource implementation.
"""
from typing import Optional, Union

from pyyoutube.error import PyYouTubeException, ErrorMessage, ErrorCode
from pyyoutube.resources.base_resource import Resource
from pyyoutube.models import Channel, ChannelListResponse
from pyyoutube.utils.params_checker import enf_comma_separated, enf_parts


class ChannelsResource(Resource):
    """A channel resource contains information about a YouTube channel.

    References: https://developers.google.com/youtube/v3/docs/channels
    """

    def list(
        self,
        parts: Optional[Union[str, list, tuple, set]] = None,
        for_username: Optional[str] = None,
        channel_id: Optional[Union[str, list, tuple, set]] = None,
        managed_by_me: Optional[bool] = None,
        mine: Optional[bool] = None,
        hl: Optional[str] = None,
        max_results: Optional[int] = None,
        on_behalf_of_content_owner: Optional[str] = None,
        page_token: Optional[str] = None,
        return_json: bool = False,
        **kwargs: Optional[dict],
    ) -> Union[dict, ChannelListResponse]:
        """Returns a collection of zero or more channel resources that match the request criteria.

        Args:
            parts:
                Comma-separated list of one or more channel resource properties.
                Accepted values: id,auditDetails,brandingSettings,contentDetails,contentOwnerDetails,
                localizations,snippet,statistics,status,topicDetails
            for_username:
                The parameter specifies a YouTube username, thereby requesting
                the channel associated with that username.
            channel_id:
                The parameter specifies a comma-separated list of the YouTube channel ID(s)
                for the resource(s) that are being retrieved.
            managed_by_me:
                Set this parameter's value to true to instruct the API to only return channels
                managed by the content owner that the onBehalfOfContentOwner parameter specifies.
                The user must be authenticated as a CMS account linked to the specified content
                owner and onBehalfOfContentOwner must be provided.
            mine:
                Set this parameter's value to true to instruct the API to only return channels
                owned by the authenticated user.
            hl:
                The hl parameter instructs the API to retrieve localized resource metadata for
                a specific application language that the YouTube website supports.
                The parameter value must be a language code included in the list returned by the
                i18nLanguages.list method.
            max_results:
                The parameter specifies the maximum number of items that should be returned
                the result set.
                Acceptable values are 0 to 50, inclusive. The default value is 5.
            on_behalf_of_content_owner:
                The onBehalfOfContentOwner parameter indicates that the request's authorization
                credentials identify a YouTube CMS user who is acting on behalf of the content
                owner specified in the parameter value. This parameter is intended for YouTube
                content partners that own and manage many difference YouTube channels. It allows
                content owners to authenticate once and get access to all their video and channel
                data, without having to provide authentication credentials for each individual channel.
                The CMS account that the user authenticates with must be linked to the specified YouTube content owner.
            page_token:
                The parameter identifies a specific page in the result set that should be returned.
            return_json:
                Type for returned data. If you set True JSON data will be returned.
            **kwargs:
                Additional parameters for system parameters.
                Refer: https://cloud.google.com/apis/docs/system-parameters.

        Returns:
            Channel data
        Raises:
            PyYouTubeException: Missing filter parameter.
                                Request not success.
        """

        params = {
            "part": enf_parts(resource="channels", value=parts),
            "hl": hl,
            "maxResults": max_results,
            "onBehalfOfContentOwner": on_behalf_of_content_owner,
            "pageToken": page_token,
            **kwargs,
        }
        if for_username is not None:
            params["forUsername"] = for_username
        elif channel_id is not None:
            params["id"] = enf_comma_separated(field="channel_id", value=channel_id)
        elif managed_by_me is not None:
            params["managedByMe"] = managed_by_me
        elif mine is not None:
            params["mine"] = mine
        else:
            raise PyYouTubeException(
                ErrorMessage(
                    status_code=ErrorCode.MISSING_PARAMS,
                    message=f"Specify at least one of for_username,channel_id,managedByMe or mine",
                )
            )

        response = self._client.request(path="channels", params=params)
        data = self._client.parse_response(response=response)
        return data if return_json else ChannelListResponse.from_dict(data)

    def update(
        self,
        part: str,
        body: Union[dict, Channel],
        on_behalf_of_content_owner: Optional[str] = None,
        return_json: bool = False,
        **kwargs,
    ) -> Union[dict, Channel]:
        """Updates a channel's metadata.

        Note that this method currently only supports updates to the channel resource's brandingSettings,
        invideoPromotion, and localizations objects and their child properties.

        Args:
            part:
                The part parameter serves two purposes in this operation. It identifies the properties
                that the write operation will set as well as the properties that the API response will include.
            body:
                Provide channel data in the request body. You can give dataclass or just a dict with data.
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
            Channel updated data.
        """

        params = {
            "part": part,
            "onBehalfOfContentOwner": on_behalf_of_content_owner,
            **kwargs,
        }
        response = self._client.request(
            method="PUT",
            path="channels",
            params=params,
            json=body,
        )
        data = self._client.parse_response(response=response)
        return data if return_json else Channel.from_dict(data)
