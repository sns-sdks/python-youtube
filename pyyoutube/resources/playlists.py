"""
    Playlist resource implementation.
"""

from typing import Optional, Union

from pyyoutube.error import PyYouTubeException, ErrorCode, ErrorMessage
from pyyoutube.resources.base_resource import Resource
from pyyoutube.models import Playlist, PlaylistListResponse
from pyyoutube.utils.params_checker import enf_comma_separated, enf_parts


class PlaylistsResource(Resource):
    """A playlist resource represents a YouTube playlist.

    References: https://developers.google.com/youtube/v3/docs/playlists
    """

    def list(
        self,
        parts: Optional[Union[str, list, tuple, set]] = None,
        channel_id: Optional[str] = None,
        playlist_id: Optional[Union[str, list, tuple, set]] = None,
        mine: Optional[bool] = None,
        hl: Optional[str] = None,
        max_results: Optional[int] = None,
        on_behalf_of_content_owner: Optional[str] = None,
        on_behalf_of_content_owner_channel: Optional[str] = None,
        page_token: Optional[str] = None,
        return_json: bool = False,
        **kwargs: Optional[dict],
    ) -> Union[dict, PlaylistListResponse]:
        """Returns a collection of playlists that match the API request parameters.

        Args:
            parts:
                Comma-separated list of one or more channel resource properties.
                Accepted values: id,contentDetails,localizations,player,snippet,status
            channel_id:
                Indicates that the API should only return the specified channel's playlists.
            playlist_id:
                Specifies a comma-separated list of the YouTube playlist ID(s) for the resource(s)
                that are being retrieved.
            mine:
                Set this parameter's value to true to instruct the API to only return playlists
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
            on_behalf_of_content_owner_channel:
                The onBehalfOfContentOwnerChannel parameter specifies the YouTube channel ID of the channel
                to which a video is being added. This parameter is required when a request specifies a value
                for the onBehalfOfContentOwner parameter, and it can only be used in conjunction with that
                parameter. In addition, the request must be authorized using a CMS account that is linked to
                the content owner that the onBehalfOfContentOwner parameter specifies. Finally, the channel
                that the onBehalfOfContentOwnerChannel parameter value specifies must be linked to the content
                owner that the onBehalfOfContentOwner parameter specifies.
            page_token:
                The parameter identifies a specific page in the result set that should be returned.
            return_json:
                Type for returned data. If you set True JSON data will be returned.
            **kwargs:
                Additional parameters for system parameters.
                Refer: https://cloud.google.com/apis/docs/system-parameters.

        Returns:
            Playlist data.
        Raises:
            PyYouTubeException: Missing filter parameter.
        """

        params = {
            "part": enf_parts(resource="playlists", value=parts),
            "hl": hl,
            "maxResults": max_results,
            "onBehalfOfContentOwner": on_behalf_of_content_owner,
            "onBehalfOfContentOwnerChannel": on_behalf_of_content_owner_channel,
            "pageToken": page_token,
            **kwargs,
        }
        if channel_id is not None:
            params["channelId"] = channel_id
        elif playlist_id is not None:
            params["id"] = enf_comma_separated(field="playlist_id", value=playlist_id)
        elif mine is not None:
            params["mine"] = mine
        else:
            raise PyYouTubeException(
                ErrorMessage(
                    status_code=ErrorCode.MISSING_PARAMS,
                    message=f"Specify at least one of channel_id, playlist_id or mine",
                )
            )
        response = self._client.request(path="playlists", params=params)
        data = self._client.parse_response(response=response)
        return data if return_json else PlaylistListResponse.from_dict(data)

    def insert(
        self,
        body: Union[dict, Playlist],
        parts: Optional[Union[str, list, tuple, set]] = None,
        on_behalf_of_content_owner: Optional[str] = None,
        on_behalf_of_content_owner_channel: Optional[str] = None,
        return_json: bool = False,
        **kwargs: Optional[dict],
    ) -> Union[dict, Playlist]:
        """Creates a playlist.

        Args:
            body:
                Provide playlist data in the request body. You can give dataclass or just a dict with data.
            parts:
                The part parameter serves two purposes in this operation. It identifies the properties
                that the write operation will set as well as the properties that the API response will include.
            on_behalf_of_content_owner:
                The onBehalfOfContentOwner parameter indicates that the request's authorization
                credentials identify a YouTube CMS user who is acting on behalf of the content
                owner specified in the parameter value. This parameter is intended for YouTube
                content partners that own and manage many difference YouTube channels. It allows
                content owners to authenticate once and get access to all their video and channel
                data, without having to provide authentication credentials for each individual channel.
                The CMS account that the user authenticates with must be linked to the specified YouTube content owner.
            on_behalf_of_content_owner_channel:
                The onBehalfOfContentOwnerChannel parameter specifies the YouTube channel ID of the channel
                to which a video is being added. This parameter is required when a request specifies a value
                for the onBehalfOfContentOwner parameter, and it can only be used in conjunction with that
                parameter. In addition, the request must be authorized using a CMS account that is linked to
                the content owner that the onBehalfOfContentOwner parameter specifies. Finally, the channel
                that the onBehalfOfContentOwnerChannel parameter value specifies must be linked to the content
                owner that the onBehalfOfContentOwner parameter specifies.
            return_json:
                Type for returned data. If you set True JSON data will be returned.
            **kwargs:
                Additional parameters for system parameters.
                Refer: https://cloud.google.com/apis/docs/system-parameters.
        Returns:
            playlist data.
        """

        params = {
            "part": enf_parts(resource="playlists", value=parts),
            "onBehalfOfContentOwner": on_behalf_of_content_owner,
            "onBehalfOfContentOwnerChannel": on_behalf_of_content_owner_channel,
            **kwargs,
        }
        response = self._client.request(
            method="POST", path="playlists", params=params, json=body
        )
        data = self._client.parse_response(response=response)
        return data if return_json else Playlist.from_dict(data)

    def update(
        self,
        body: Union[dict, Playlist],
        parts: Optional[Union[str, list, tuple, set]] = None,
        on_behalf_of_content_owner: Optional[str] = None,
        return_json: bool = False,
        **kwargs: Optional[dict],
    ) -> Union[dict, Playlist]:
        """Modifies a playlist.

        Args:
            body:
                Provide playlist data in the request body. You can give dataclass or just a dict with data.
            parts:
                The part parameter serves two purposes in this operation. It identifies the properties
                that the write operation will set as well as the properties that the API response will include.
            on_behalf_of_content_owner:
                The onBehalfOfContentOwner parameter indicates that the request's authorization
                credentials identify a YouTube CMS user who is acting on behalf of the content
                owner specified in the parameter value. This parameter is intended for YouTube
                content partners that own and manage many difference YouTube channels. It allows
                content owners to authenticate once and get access to all their video and channel
                data, without having to provide authentication credentials for each individual channel.
                The CMS account that the user authenticates with must be linked to the specified YouTube content owner.
            return_json:
                Type for returned data. If you set True JSON data will be returned.
            **kwargs:
                Additional parameters for system parameters.
                Refer: https://cloud.google.com/apis/docs/system-parameters.

        Returns:
            Playlist updated data.

        """
        params = {
            "part": enf_parts(resource="playlists", value=parts),
            "onBehalfOfContentOwner": on_behalf_of_content_owner,
            **kwargs,
        }
        response = self._client.request(
            method="PUT", path="playlists", params=params, json=body
        )
        data = self._client.parse_response(response=response)
        return data if return_json else Playlist.from_dict(data)

    def delete(
        self,
        playlist_id: str,
        on_behalf_of_content_owner: Optional[str] = None,
        **kwargs: Optional[dict],
    ) -> bool:
        """Deletes a playlist.

        Args:
            playlist_id:
                Specifies the YouTube playlist ID for the playlist that is being deleted.
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
            playlist delete status

        """
        params = {
            "id": playlist_id,
            "onBehalfOfContentOwner": on_behalf_of_content_owner,
            **kwargs,
        }
        response = self._client.request(
            method="DELETE",
            path="playlists",
            params=params,
        )
        if response.ok:
            return True
        self._client.parse_response(response=response)
