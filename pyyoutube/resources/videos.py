"""
    Videos resource implementation.
"""

from typing import Optional, Union

from pyyoutube.error import PyYouTubeException, ErrorCode, ErrorMessage
from pyyoutube.resources.base_resource import Resource
from pyyoutube.media import Media, MediaUpload
from pyyoutube.models import (
    Video,
    VideoListResponse,
    VideoGetRatingResponse,
    VideoReportAbuse,
)
from pyyoutube.utils.params_checker import enf_comma_separated, enf_parts


class VideosResource(Resource):
    """A video resource represents a YouTube video.

    References: https://developers.google.com/youtube/v3/docs/videos
    """

    def list(
        self,
        parts: Optional[Union[str, list, tuple, set]] = None,
        chart: Optional[str] = None,
        video_id: Optional[Union[str, list, tuple, set]] = None,
        my_rating: Optional[str] = None,
        hl: Optional[str] = None,
        max_height: Optional[int] = None,
        max_results: Optional[int] = None,
        max_width: Optional[int] = None,
        on_behalf_of_content_owner: Optional[str] = None,
        page_token: Optional[str] = None,
        region_code: Optional[str] = None,
        video_category_id: Optional[str] = None,
        return_json: bool = False,
        **kwargs: Optional[dict],
    ) -> Union[dict, VideoListResponse]:
        """Returns a list of videos that match the API request parameters.

        Args:
            parts:
                Comma-separated list of one or more channel resource properties.
                Accepted values: id,contentDetails,fileDetails,liveStreamingDetails,
                localizations,player,processingDetails,recordingDetails,snippet,statistics,
                status,suggestions,topicDetails
            chart:
                Identifies the chart that you want to retrieve.
                Acceptable values are:
                    - mostPopular:  Return the most popular videos for the specified content region and video category.
            video_id:
                Specifies a comma-separated list of the YouTube video ID(s) for the resource(s) that are being retrieved.
            my_rating:
                Set this parameter's value to like or dislike to instruct the API to only return videos liked
                or disliked by the authenticated user.
                Acceptable values are:
                    - dislike: Returns only videos disliked by the authenticated user.
                    - like: Returns only video liked by the authenticated user.
            hl:
                Instructs the API to retrieve localized resource metadata for a specific application language
                that the YouTube website supports.
            max_height:
                Specifies the maximum height of the embedded player returned the player.embedHtml property.
            max_results:
                Specifies the maximum number of items that should be returned the result set.
            max_width:
                Specifies the maximum width of the embedded player returned the player.embedHtml property.
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
            region_code:
                Instructs the API to select a video chart available in the specified region.
            video_category_id:
                Identifies the video category for which the chart should be retrieved.
            return_json:
                Type for returned data. If you set True JSON data will be returned.
            **kwargs:
                Additional parameters for system parameters.
                Refer: https://cloud.google.com/apis/docs/system-parameters.

        Returns:
            Videos data.
        Raises:
            PyYouTubeException: Missing filter parameter.
        """
        params = {
            "part": enf_parts(resource="videos", value=parts),
            "hl": hl,
            "maxHeight": max_height,
            "maxResults": max_results,
            "maxWidth": max_width,
            "onBehalfOfContentOwner": on_behalf_of_content_owner,
            "pageToken": page_token,
            "regionCode": region_code,
            "videoCategoryId": video_category_id,
            **kwargs,
        }
        if chart is not None:
            params["chart"] = chart
        elif video_id is not None:
            params["id"] = enf_comma_separated(field="video_id", value=video_id)
        elif my_rating is not None:
            params["myRating"] = my_rating
        else:
            raise PyYouTubeException(
                ErrorMessage(
                    status_code=ErrorCode.MISSING_PARAMS,
                    message=f"Specify at least one of for_username,channel_id,managedByMe or mine",
                )
            )
        response = self._client.request(path="videos", params=params)
        data = self._client.parse_response(response=response)
        return data if return_json else VideoListResponse.from_dict(data)

    def insert(
        self,
        body: Union[dict, Video],
        media: Media,
        parts: Optional[Union[str, list, tuple, set]] = None,
        notify_subscribers: Optional[bool] = None,
        on_behalf_of_content_owner: Optional[str] = None,
        on_behalf_of_content_owner_channel: Optional[str] = None,
        **kwargs,
    ) -> MediaUpload:
        """Uploads a video to YouTube and optionally sets the video's metadata.

        Example:

            import pyyoutube.models as mds
            from pyyoutube.media import Media

            body = mds.Video(
                snippet=mds.VideoSnippet(
                    title="video title",
                    description="video description"
                )
            )

            media = Media(filename="video.mp4")

            upload = client.videos.insert(
                body=body,
                media=media,
                parts=["snippet"],
            )

            response = None
            while response is None:
                status, response = upload.next_chunk()
                if status:
                    print(f"Upload {int(status.progress() * 100)} complete.")

            print(f"Response body: {response}")

        Args:
            body:
                Provide video data in the request body. You can give dataclass or just a dict with data.
            media:
                Media data to upload.
            parts:
                Comma-separated list of one or more channel resource properties.
                Accepted values: id,contentDetails,fileDetails,liveStreamingDetails,
                localizations,player,processingDetails,recordingDetails,snippet,statistics,
                status,suggestions,topicDetails
            notify_subscribers:
                Indicates whether YouTube should send a notification about the new video to users who
                subscribe to the video's channel
            on_behalf_of_content_owner:
                The onBehalfOfContentOwner parameter indicates that the request's authorization
                credentials identify a YouTube CMS user who is acting on behalf of the content
                owner specified in the parameter value. This parameter is intended for YouTube
                content partners that own and manage many different YouTube channels. It allows
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
            **kwargs:
                Additional parameters for system parameters.
                Refer: https://cloud.google.com/apis/docs/system-parameters.
        Returns:
            Video data.

        """
        params = {
            "part": enf_parts(resource="videos", value=parts),
            "notifySubscribers": notify_subscribers,
            "onBehalfOfContentOwner": on_behalf_of_content_owner,
            "onBehalfOfContentOwnerChannel": on_behalf_of_content_owner_channel,
            **kwargs,
        }

        # Build a media upload instance.
        media_upload = MediaUpload(
            client=self._client,
            resource="videos",
            media=media,
            params=params,
            body=body.to_dict_ignore_none(),
        )
        return media_upload

    def update(
        self,
        body: Union[dict, Video],
        parts: Optional[Union[str, list, tuple, set]] = None,
        on_behalf_of_content_owner: Optional[str] = None,
        return_json: bool = False,
        **kwargs: Optional[dict],
    ) -> Union[dict, Video]:
        """Updates a video's metadata.

        Args:
            body:
                Provide video data in the request body. You can give dataclass or just a dict with data.
            parts:
                Comma-separated list of one or more channel resource properties.
                Accepted values: id,contentDetails,fileDetails,liveStreamingDetails,
                localizations,player,processingDetails,recordingDetails,snippet,statistics,
                status,suggestions,topicDetails
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
            Video updated data.
        """
        params = {
            "part": enf_parts(resource="videos", value=parts),
            "onBehalfOfContentOwner": on_behalf_of_content_owner,
            **kwargs,
        }
        response = self._client.request(
            method="PUT",
            path="videos",
            params=params,
            json=body,
        )
        data = self._client.parse_response(response=response)
        return data if return_json else Video.from_dict(data)

    def rate(
        self,
        video_id: str,
        rating: Optional[str] = None,
        **kwargs: Optional[dict],
    ) -> bool:
        """Add a like or dislike rating to a video or remove a rating from a video.

        Args:
            video_id:
                Specifies the YouTube video ID of the video that is being rated or having its rating removed.
            rating:
                Specifies the rating to record.
                Acceptable values are:
                    - dislike: Records that the authenticated user disliked the video.
                    - like: Records that the authenticated user liked the video.
                    - none: Removes any rating that the authenticated user had previously set for the video.
            **kwargs:
                Additional parameters for system parameters.
                Refer: https://cloud.google.com/apis/docs/system-parameters.

        Returns:
            Video rating status
        """
        params = {
            "id": video_id,
            "rating": rating,
            **kwargs,
        }
        response = self._client.request(
            method="POST",
            path="videos/rate",
            params=params,
        )
        if response.ok:
            return True
        self._client.parse_response(response=response)

    def get_rating(
        self,
        video_id: Union[str, list, tuple, set],
        on_behalf_of_content_owner: Optional[str] = None,
        return_json: bool = False,
        **kwargs: Optional[dict],
    ) -> Union[dict, VideoGetRatingResponse]:
        """Retrieves the ratings that the authorized user gave to a list of specified videos.

        Args:
            video_id:
                Specifies a comma-separated list of the YouTube video ID(s).
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
            Video rating data.
        """

        params = {
            "id": enf_comma_separated(field="video_id", value=video_id),
            "onBehalfOfContentOwner": on_behalf_of_content_owner,
            **kwargs,
        }
        response = self._client.request(path="videos/getRating", params=params)
        data = self._client.parse_response(response=response)
        return data if return_json else VideoGetRatingResponse.from_dict(data)

    def report_abuse(
        self,
        body: Optional[Union[dict, VideoReportAbuse]],
        on_behalf_of_content_owner: Optional[str] = None,
        **kwargs: Optional[dict],
    ) -> bool:
        """Reports a video for containing abusive content.

        Args:
            body:
                Provide report abuse data in the request body. You can give dataclass or just a dict with data.
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
            report status.
        """
        params = {
            "onBehalfOfContentOwner": on_behalf_of_content_owner,
            **kwargs,
        }
        response = self._client.request(
            method="POST",
            path="videos/reportAbuse",
            params=params,
            json=body,
        )
        if response.ok:
            return True
        self._client.parse_response(response=response)

    def delete(
        self,
        video_id: str,
        on_behalf_of_content_owner: Optional[str] = None,
        **kwargs: Optional[dict],
    ) -> bool:
        """Deletes a YouTube video.

        Args:
            video_id:
                Specifies the YouTube video ID for the resource that is being deleted.
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
            video delete status.
        """
        params = {
            "id": video_id,
            "onBehalfOfContentOwner": on_behalf_of_content_owner,
            **kwargs,
        }
        response = self._client.request(
            method="DELETE",
            path="videos",
            params=params,
        )
        if response.ok:
            return True
        self._client.parse_response(response=response)
