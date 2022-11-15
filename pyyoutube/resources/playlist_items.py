"""
    Playlist items resource implementation.
"""

from typing import Optional, Union

from pyyoutube.error import PyYouTubeException, ErrorCode, ErrorMessage
from pyyoutube.resources.base_resource import Resource
from pyyoutube.models import PlaylistItem, PlaylistItemListResponse
from pyyoutube.utils.params_checker import enf_parts, enf_comma_separated


class PlaylistItemsResource(Resource):
    """A playlistItem resource identifies another resource, such as a video, that is included
    in a playlist. In addition, the playlistItem resource contains details about the included
    resource that pertain specifically to how that resource is used in that playlist.

    References: https://developers.google.com/youtube/v3/docs/playlistItems
    """

    def list(
        self,
        parts: Optional[Union[str, list, tuple, set]] = None,
        playlist_item_id: Optional[Union[str, list, tuple, set]] = None,
        playlist_id: Optional[str] = None,
        max_results: Optional[int] = None,
        on_behalf_of_content_owner: Optional[str] = None,
        page_token: Optional[str] = None,
        video_id: Optional[str] = None,
        return_json: bool = False,
        **kwargs: Optional[dict],
    ) -> Union[dict, PlaylistItemListResponse]:
        """Returns a collection of playlist items that match the API request parameters.

        Args:
            parts:
                Comma-separated list of one or more channel resource properties.
                Accepted values: id,contentDetails,snippet,snippet
            playlist_item_id:
                Specifies a comma-separated list of one or more unique playlist item IDs.
            playlist_id:
                Specifies the unique ID of the playlist for which you want to retrieve playlist items.
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
            video_id:
                Specifies that the request should return only the playlist items that contain the specified video.
            return_json:
                Type for returned data. If you set True JSON data will be returned.
            **kwargs:
                Additional parameters for system parameters.
                Refer: https://cloud.google.com/apis/docs/system-parameters.

        Returns:
            Playlist items data.

        Raises:
            PyYouTubeException: Missing filter parameter.
        """

        params = {
            "part": enf_parts(resource="playlistItems", value=parts),
            "maxResults": max_results,
            "onBehalfOfContentOwner": on_behalf_of_content_owner,
            "videoId": video_id,
            "pageToken": page_token,
            **kwargs,
        }
        if playlist_item_id is not None:
            params["id"] = enf_comma_separated(
                field="playlist_item_id", value=playlist_item_id
            )
        elif playlist_id is not None:
            params["playlistId"] = playlist_id
        else:
            raise PyYouTubeException(
                ErrorMessage(
                    status_code=ErrorCode.MISSING_PARAMS,
                    message=f"Specify at least one of playlist_item_id or playlist_id",
                )
            )

        response = self._client.request(path="playlistItems", params=params)
        data = self._client.parse_response(response=response)
        return data if return_json else PlaylistItemListResponse.from_dict(data)

    def insert(
        self,
        body: Union[dict, PlaylistItem],
        parts: Optional[Union[str, list, tuple, set]] = None,
        on_behalf_of_content_owner: Optional[str] = None,
        return_json: bool = False,
        **kwargs: Optional[dict],
    ) -> Union[dict, PlaylistItem]:
        """Adds a resource to a playlist.

        Args:
            body:
                Provide playlist item data in the request body. You can give dataclass or just a dict with data.
            parts:
                Comma-separated list of one or more channel resource properties.
                Accepted values: id,contentDetails,snippet,snippet
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
            Playlist item data.
        """
        params = {
            "part": enf_parts(resource="playlistItems", value=parts),
            "onBehalfOfContentOwner": on_behalf_of_content_owner,
            **kwargs,
        }
        response = self._client.request(
            method="POST",
            path="playlistItems",
            params=params,
            json=body,
        )
        data = self._client.parse_response(response=response)
        return data if return_json else PlaylistItem.from_dict(data)

    def update(
        self,
        body: Union[dict, PlaylistItem],
        parts: Optional[Union[str, list, tuple, set]] = None,
        on_behalf_of_content_owner: Optional[str] = None,
        return_json: bool = False,
        **kwargs: Optional[dict],
    ) -> Union[dict, PlaylistItem]:
        """Modifies a playlist item. For example, you could update the item's position in the playlist.

        Args:
            body:
                Provide playlist item data in the request body. You can give dataclass or just a dict with data.
            parts:
                Comma-separated list of one or more channel resource properties.
                Accepted values: id,contentDetails,snippet,snippet
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
            Playlist item update data.
        """
        params = {
            "part": enf_parts(resource="playlistItems", value=parts),
            "onBehalfOfContentOwner": on_behalf_of_content_owner,
            **kwargs,
        }
        response = self._client.request(
            method="PUT",
            path="playlistItems",
            params=params,
            json=body,
        )
        data = self._client.parse_response(response=response)
        return data if return_json else PlaylistItem.from_dict(data)

    def delete(
        self,
        playlist_item_id: str,
        on_behalf_of_content_owner: Optional[str] = None,
        **kwargs: Optional[dict],
    ) -> bool:
        """Deletes a playlist item.

        Args:
            playlist_item_id:
                Specifies the YouTube playlist item ID for the playlist item that is being deleted.
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
            Playlist item delete status.

        """
        params = {
            "id": playlist_item_id,
            "onBehalfOfContentOwner": on_behalf_of_content_owner,
            **kwargs,
        }
        response = self._client.request(
            method="DELETE",
            path="playlistItems",
            params=params,
        )
        if response.ok:
            return True
        self._client.parse_response(response=response)
