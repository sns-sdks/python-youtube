"""
    Search resource implementation.
"""
from typing import Optional, Union

from pyyoutube.resources.base_resource import Resource
from pyyoutube.models import SearchListResponse
from pyyoutube.utils.params_checker import enf_parts


class SearchResource(Resource):
    """A search result contains information about a YouTube video, channel, or playlist
    that matches the search parameters specified in an API request

    References: https://developers.google.com/youtube/v3/docs/search
    """

    def list(
        self,
        parts: Optional[Union[str, list, tuple, set]] = None,
        for_content_owner: Optional[bool] = None,
        for_developer: Optional[bool] = None,
        for_mine: Optional[bool] = None,
        related_to_video_id: Optional[str] = None,
        channel_id: Optional[str] = None,
        channel_type: Optional[str] = None,
        event_type: Optional[str] = None,
        location: Optional[str] = None,
        location_radius: Optional[str] = None,
        max_results: Optional[int] = None,
        on_behalf_of_content_owner: Optional[str] = None,
        order: Optional[str] = None,
        page_token: Optional[str] = None,
        published_after: Optional[str] = None,
        published_before: Optional[str] = None,
        q: Optional[str] = None,
        region_code: Optional[str] = None,
        relevance_language: Optional[str] = None,
        safe_search: Optional[str] = None,
        topic_id: Optional[str] = None,
        type: Optional[Union[str, list, tuple, set]] = None,
        video_caption: Optional[str] = None,
        video_category_id: Optional[str] = None,
        video_definition: Optional[str] = None,
        video_dimension: Optional[str] = None,
        video_duration: Optional[str] = None,
        video_embeddable: Optional[str] = None,
        video_license: Optional[str] = None,
        video_paid_product_placement: Optional[str] = None,
        video_syndicated: Optional[str] = None,
        video_type: Optional[str] = None,
        return_json: bool = False,
        **kwargs: Optional[dict],
    ) -> Union[dict, SearchListResponse]:
        """Returns a collection of search results that match the query parameters specified in the API request.

        Notes:
            Search API is very complex. If you want to search, You may need to read the parameter description
            with the docs: https://developers.google.com/youtube/v3/docs/search/list#parameters

        Args:
            parts:
                Comma-separated list of one or more channel resource properties.
                Accepted values: snippet
            for_content_owner:
                Parameter restricts the search to only retrieve videos owned by the content owner
                identified by the onBehalfOfContentOwner parameter.
            for_developer:
                Parameter restricts the search to only retrieve videos uploaded via the developer's
                application or website.
            for_mine:
                Parameter restricts the search to only retrieve videos owned by the authenticated user.
            related_to_video_id:
                Parameter retrieves a list of videos that are related to the video that the parameter value identifies.
                Deprecated at [2023.08.07](https://developers.google.com/youtube/v3/revision_history#august-7,-2023)
            channel_id:
                Indicates that the API response should only contain resources created by the channel.
            channel_type:
                Parameter lets you restrict a search to a particular type of channel.
                Acceptable values are:
                    - any: Return all channels.
                    - show: Only retrieve shows.
            event_type:
                Parameter restricts a search to broadcast events.
                Acceptable values are:
                    - completed: Only include completed broadcasts.
                    - live: Only include active broadcasts.
                    - upcoming: Only include upcoming broadcasts.
            location:
                Parameter value identifies the point at the center of the area.
            location_radius:
                Specifies the maximum distance that the location associated with a video can be from
                that point for the video to still be included in the search results.
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
            order:
                Specifies the method that will be used to order resources in the API response.
                The default value is relevance.
                Acceptable values are:
                    - date: Resources are sorted in reverse chronological order based on the date they were created.
                    - rating: Resources are sorted from highest to lowest rating.
                    - relevance: Resources are sorted based on their relevance to the search query.
                    - title: Resources are sorted alphabetically by title.
                    - videoCount: Channels are sorted in descending order of their number of uploaded videos.
                    - viewCount: Resources are sorted from highest to lowest number of views.
                    For live broadcasts, videos are sorted by number of concurrent viewers while the broadcasts
                    are ongoing.
            page_token:
                The parameter identifies a specific page in the result set that should be returned.
            published_after:
                Indicates that the API response should only contain resources created at or after the specified time.
            published_before:
                Indicates that the API response should only contain resources created before or at the specified time.
            q:
                Specifies the query term to search for.
            region_code:
                Instructs the API to return search results for videos that can be viewed in the specified country.
            relevance_language:
                Instructs the API to return search results that are most relevant to the specified language.
            safe_search:
                Indicates whether the search results should include restricted content as well as standard content.
                Acceptable values are:
                    - moderate: YouTube will filter some content from search results and, at the least,
                        will filter content that is restricted in your locale. Based on their content, search
                        results could be removed from search results or demoted in search results.
                        This is the default parameter value.
                    - none: YouTube will not filter the search result set.
                    - strict: YouTube will try to exclude all restricted content from the search result set.
                        Based on their content, search results could be removed from search results or
                        demoted in search results.
            topic_id:
                Indicates that the API response should only contain resources associated with the specified topic.
            type:
                Parameter restricts a search query to only retrieve a particular type of resource.
                The value is a comma-separated list of resource types.
                Acceptable values are: channel,playlist,video
            video_caption:
                Indicates whether the API should filter video search results based on whether they have captions.
                Acceptable values are:
                    - any: Do not filter results based on caption availability.
                    - closedCaption: Only include videos that have captions.
                    - none: Only include videos that do not have captions.
            video_category_id:
                Parameter filters video search results based on their category.
            video_definition:
                Parameter lets you restrict a search to only include either high definition (HD) or
                standard definition (SD) videos.
                Acceptable values are:
                    - any: Return all videos, regardless of their resolution.
                    - high: Only retrieve HD videos.
                    - standard: Only retrieve videos in standard definition.
            video_dimension:
                Parameter lets you restrict a search to only retrieve 2D or 3D videos.
                Acceptable values are:
                    - 2d: Restrict search results to exclude 3D videos.
                    - 3d: Restrict search results to only include 3D videos.
                    - any: Include both 3D and non-3D videos in returned results. This is the default value.
            video_duration:
                Parameter filters video search results based on their duration.
                Acceptable values are:
                    - any: Do not filter video search results based on their duration. This is the default value.
                    - long: Only include videos longer than 20 minutes.
                    - medium: Only include videos that are between four and 20 minutes long (inclusive).
                    - short: Only include videos that are less than four minutes long.
            video_embeddable:
                Parameter lets you to restrict a search to only videos that can be embedded into a webpage.
                Acceptable values are:
                    - any: Return all videos, embeddable or not.
                    - true: Only retrieve embeddable videos.
            video_license:
                Parameter filters search results to only include videos with a particular license.
                Acceptable values are:
                    - any – Return all videos, regardless of which license they have, that match the query parameters.
                    - creativeCommon – Only return videos that have a Creative Commons license.
                        Users can reuse videos with this license in other videos that they create. Learn more.
                    - youtube – Only return videos that have the standard YouTube license.
            video_paid_product_placement:
                Parameter filters search results to only include videos that the creator has denoted as
                having a paid promotion.
                Acceptable values are:
                    - any – Return all videos, regardless of whether they contain paid promotions.
                    - true – Only retrieve videos with paid promotions.
            video_syndicated:
                Parameter lets you to restrict a search to only videos that can be played outside youtube.com.
                Acceptable values are:
                    - any: Return all videos, syndicated or not.
                    - true: Only retrieve syndicated videos.
            video_type:
                Parameter lets you restrict a search to a particular type of videos.
                Acceptable values are:
                    - any: Return all videos.
                    - episode: Only retrieve episodes of shows.
                    - movie: Only retrieve movies.
            return_json:
                Type for returned data. If you set True JSON data will be returned.
            **kwargs:
                Additional parameters for system parameters.
                Refer: https://cloud.google.com/apis/docs/system-parameters.
        Returns:
            Search result data

        """

        params = {
            "part": enf_parts(resource="search", value=parts),
            "channelId": channel_id,
            "channelType": channel_type,
            "eventType": event_type,
            "location": location,
            "locationRadius": location_radius,
            "maxResults": max_results,
            "onBehalfOfContentOwner": on_behalf_of_content_owner,
            "order": order,
            "pageToken": page_token,
            "publishedAfter": published_after,
            "publishedBefore": published_before,
            "q": q,
            "regionCode": region_code,
            "relevanceLanguage": relevance_language,
            "safeSearch": safe_search,
            "topicId": topic_id,
            "type": type,
            "videoCaption": video_caption,
            "videoCategoryId": video_category_id,
            "videoDefinition": video_definition,
            "videoDimension": video_dimension,
            "videoDuration": video_duration,
            "videoEmbeddable": video_embeddable,
            "videoLicense": video_license,
            "videoPaidProductPlacement": video_paid_product_placement,
            "videoSyndicated": video_syndicated,
            "videoType": video_type,
            **kwargs,
        }

        if for_content_owner is not None:
            params["forContentOwner"] = for_content_owner
        elif for_developer is not None:
            params["forDeveloper"] = for_developer
        elif for_mine is not None:
            params["forMine"] = for_mine
        elif related_to_video_id is not None:
            params["relatedToVideoId"] = related_to_video_id

        response = self._client.request(path="search", params=params)
        data = self._client.parse_response(response=response)
        return data if return_json else SearchListResponse.from_dict(data)
