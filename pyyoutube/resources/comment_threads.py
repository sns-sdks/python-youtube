"""
    Comment threads resource implementation.
"""
from typing import Optional, Union

from pyyoutube.error import PyYouTubeException, ErrorMessage, ErrorCode
from pyyoutube.resources.base_resource import Resource
from pyyoutube.models import CommentThread, CommentThreadListResponse
from pyyoutube.utils.params_checker import enf_parts


class CommentThreadsResource(Resource):
    """A commentThread resource contains information about a YouTube comment thread, which comprises a
    top-level comment and replies, if any exist, to that comment

    References: https://developers.google.com/youtube/v3/docs/commentThreads
    """

    def list(
        self,
        parts: Optional[Union[str, list, tuple, set]] = None,
        all_threads_related_to_channel_id: Optional[str] = None,
        channel_id: Optional[str] = None,
        thread_id: Optional[Union[str, list, tuple, set]] = None,
        video_id: Optional[str] = None,
        max_results: Optional[int] = None,
        moderation_status: Optional[str] = None,
        order: Optional[str] = None,
        page_token: Optional[str] = None,
        search_terms: Optional[str] = None,
        text_format: Optional[str] = None,
        return_json: bool = False,
        **kwargs: Optional[dict],
    ) -> Union[dict, CommentThreadListResponse]:
        """Returns a list of comment threads that match the API request parameters.

        Args:
            parts:
                Comma-separated list of one or more comment thread resource properties.
            all_threads_related_to_channel_id:
                Instructs the API to return all comment threads associated with the specified channel.
            channel_id:
                Instructs the API to return comment threads containing comments about the specified channel
            thread_id:
                Specifies a comma-separated list of comment thread IDs for the resources that should be retrieved.
            video_id:
                Instructs the API to return comment threads associated with the specified video ID.
            max_results:
                The parameter specifies the maximum number of items that should be returned
                the result set.
                Acceptable values are 1 to 100, inclusive. The default value is 20.
            moderation_status:
                Set this parameter to limit the returned comment threads to a particular moderation state.
                The default value is published.
                Note: This parameter is not supported for use in conjunction with the id parameter.
            order:
                Specifies the order in which the API response should list comment threads.
                Valid values are:
                    - time: Comment threads are ordered by time. This is the default behavior.
                    - relevance: Comment threads are ordered by relevance.
                Notes: This parameter is not supported for use in conjunction with the `id` parameter.
            page_token:
                 Identifies a specific page in the result set that should be returned.
                 Notes: This parameter is not supported for use in conjunction with the `id` parameter.
            search_terms:
                 Instructs the API to limit the API response to only contain comments that contain
                 the specified search terms.
                 Notes: This parameter is not supported for use in conjunction with the `id` parameter.
            text_format:
                Set this parameter's value to html or plainText to instruct the API to return the comments
                left by users in html formatted or in plain text. The default value is html.
                Acceptable values are:
                    – html: Returns the comments in HTML format. This is the default value.
                    – plainText: Returns the comments in plain text format.
                Notes: This parameter is not supported for use in conjunction with the `id` parameter.
            return_json:
                Type for returned data. If you set True JSON data will be returned.
            **kwargs:
                Additional parameters for system parameters.
                Refer: https://cloud.google.com/apis/docs/system-parameters.

        Returns:
            Comment threads data.
        Raises:
            PyYouTubeException: Missing filter parameter.
        """

        params = {
            "part": enf_parts(resource="commentThreads", value=parts),
            "maxResults": max_results,
            "moderationStatus": moderation_status,
            "order": order,
            "pageToken": page_token,
            "searchTerms": search_terms,
            "textFormat": text_format,
            **kwargs,
        }
        if all_threads_related_to_channel_id is not None:
            params["allThreadsRelatedToChannelId"] = all_threads_related_to_channel_id
        elif channel_id:
            params["channelId"] = channel_id
        elif thread_id:
            params["id"] = thread_id
        elif video_id:
            params["videoId"] = video_id
        else:
            raise PyYouTubeException(
                ErrorMessage(
                    status_code=ErrorCode.MISSING_PARAMS,
                    message="Specify at least one of all_threads_related_to_channel_id, channel_id, thread_id or video_id",
                )
            )
        response = self._client.request(path="commentThreads", params=params)
        data = self._client.parse_response(response=response)
        return data if return_json else CommentThreadListResponse.from_dict(data)

    def insert(
        self,
        body: Union[dict, CommentThread],
        parts: Optional[Union[str, list, tuple, set]] = None,
        return_json: bool = False,
        **kwargs,
    ) -> Union[dict, CommentThread]:
        """Creates a new top-level comment.

        Notes: To add a reply to an existing comment, use the comments.insert method instead.

        Args:
            body:
                Provide a commentThread resource in the request body. You can give dataclass or just a dict with data.
            parts:
                Comma-separated list of one or more comment thread resource properties.
            return_json:
                Type for returned data. If you set True JSON data will be returned.
            **kwargs:
                Additional parameters for system parameters.
                Refer: https://cloud.google.com/apis/docs/system-parameters.

        Returns:
            Channel thread data.

        """
        params = {
            "part": enf_parts(resource="commentThreads", value=parts),
            **kwargs,
        }

        response = self._client.request(
            method="POST",
            path="commentThreads",
            params=params,
            json=body,
        )
        data = self._client.parse_response(response=response)
        return data if return_json else CommentThread.from_dict(data)
