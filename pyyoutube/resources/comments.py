"""
    Comment resource implementation.
"""

from typing import Optional, Union

from pyyoutube.error import PyYouTubeException, ErrorMessage, ErrorCode
from pyyoutube.resources.base_resource import Resource
from pyyoutube.models import Comment, CommentListResponse
from pyyoutube.utils.params_checker import enf_comma_separated, enf_parts


class CommentsResource(Resource):
    """A comment resource contains information about a single YouTube comment.

    References: https://developers.google.com/youtube/v3/docs/comments
    """

    def list(
        self,
        parts: Optional[Union[str, list, tuple, set]] = None,
        comment_id: Optional[Union[str, list, tuple, set]] = None,
        parent_id: Optional[str] = None,
        max_results: Optional[int] = None,
        text_format: Optional[str] = None,
        page_token: Optional[str] = None,
        return_json: bool = False,
        **kwargs: Optional[dict],
    ) -> Union[dict, CommentListResponse]:
        """Returns a list of comments that match the API request parameters.

        Args:
            parts:
                Comma-separated list of one or more comment resource properties.
            comment_id:
                Specifies a comma-separated list of comment IDs for the resources that are being retrieved.
            parent_id:
                Specifies the ID of the comment for which replies should be retrieved.
            max_results:
                The parameter specifies the maximum number of items that should be returned
                the result set.
                This parameter is not supported for use in conjunction with the comment_id parameter.
                Acceptable values are 1 to 100, inclusive. The default value is 20.
            text_format:
                Whether the API should return comments formatted as HTML or as plain text.
                The default value is html.
                Acceptable values are:
                    - html: Returns the comments in HTML format.
                    - plainText: Returns the comments in plain text format.
            page_token:
                The parameter identifies a specific page in the result set that should be returned.
            return_json:
                Type for returned data. If you set True JSON data will be returned.
            kwargs:
                Additional parameters for system parameters.
                Refer: https://cloud.google.com/apis/docs/system-parameters.

        Returns:
            Comments data
        Raises:
            PyYouTubeException: Missing filter parameter.
        """

        params = {
            "part": enf_parts(resource="comments", value=parts),
            "maxResults": max_results,
            "textFormat": text_format,
            "pageToken": page_token,
            **kwargs,
        }
        if comment_id is not None:
            params["id"] = enf_comma_separated(field="comment_id", value=comment_id)
        elif parent_id is not None:
            params["parentId"] = parent_id
        else:
            raise PyYouTubeException(
                ErrorMessage(
                    status_code=ErrorCode.MISSING_PARAMS,
                    message=f"Specify at least one of for_username, id, managedByMe or mine",
                )
            )

        response = self._client.request(path="comments", params=params)
        data = self._client.parse_response(response=response)
        return data if return_json else CommentListResponse.from_dict(data)

    def insert(
        self,
        body: Union[dict, Comment],
        parts: Optional[Union[str, list, tuple, set]] = None,
        return_json: bool = False,
        **kwargs,
    ) -> Union[dict, Comment]:
        """Creates a reply to an existing comment.

        Notes:
            To create a top-level comment, use the commentThreads.insert method.

        Args:
            body:
                Provide a comment resource in the request body. You can give dataclass or just a dict with data.
            parts:
                Comma-separated list of one or more comment resource properties.
            return_json:
                Type for returned data. If you set True JSON data will be returned.
            **kwargs:
                Additional parameters for system parameters.
                Refer: https://cloud.google.com/apis/docs/system-parameters.

        Returns:
            Comment data.
        """

        params = {"part": enf_parts(resource="comments", value=parts), **kwargs}
        response = self._client.request(
            method="POST",
            path="comments",
            params=params,
            json=body,
        )
        data = self._client.parse_response(response=response)
        return data if return_json else Comment.from_dict(data)

    def update(
        self,
        body: Union[dict, Comment],
        parts: Optional[Union[str, list, tuple, set]] = None,
        return_json: bool = False,
        **kwargs,
    ) -> Union[dict, Comment]:
        """Modifies a comment.

        Args:
            body:
                Provide a comment resource in the request body. You can give dataclass or just a dict with data.
            parts:
                Comma-separated list of one or more comment resource properties.
            return_json:
                Type for returned data. If you set True JSON data will be returned.
            **kwargs:
                Additional parameters for system parameters.
                Refer: https://cloud.google.com/apis/docs/system-parameters.

        Returns:
            Comment updated data.

        """
        params = {"part": enf_parts(resource="comments", value=parts), **kwargs}
        response = self._client.request(
            method="PUT",
            path="comments",
            params=params,
            json=body,
        )
        data = self._client.parse_response(response=response)
        return data if return_json else Comment.from_dict(data)

    def mark_as_spam(
        self,
        comment_id: str,
        **kwargs,
    ) -> bool:
        """Expresses the caller's opinion that one or more comments should be flagged as spam.

        Deprecated at [2023.09.12](https://developers.google.com/youtube/v3/revision_history#september-12,-2023)

        Args:
            comment_id:
                ID for the target comment.
            **kwargs:
                Additional parameters for system parameters.
                Refer: https://cloud.google.com/apis/docs/system-parameters.

        Returns:
            Mark as spam status.

        """
        params = {"id": comment_id, **kwargs}
        response = self._client.request(
            method="POST",
            path="comments/markAsSpam",
            params=params,
        )
        if response.ok:
            return True
        self._client.parse_response(response=response)

    def set_moderation_status(
        self,
        comment_id: str,
        moderation_status: str,
        ban_author: Optional[bool] = None,
        **kwargs,
    ) -> bool:
        """Sets the moderation status of one or more comments.

        Args:
            comment_id:
                ID for the target comment.
            moderation_status:
                Identifies the new moderation status of the specified comments.
                Acceptable values:
                    - heldForReview: Marks a comment as awaiting review by a moderator.
                    - published: Clears a comment for public display.
                    - rejected:  Rejects a comment as being unfit for display.
                        This action also effectively hides all replies to the rejected comment.
            ban_author:
                Set the parameter value to true to ban the author.
                 This parameter is only valid if the moderationStatus parameter is also set to rejected.
            **kwargs:
                Additional parameters for system parameters.
                Refer: https://cloud.google.com/apis/docs/system-parameters.

        Returns:
            Moderation status set status.
        """
        params = {
            "id": comment_id,
            "moderationStatus": moderation_status,
            "banAuthor": ban_author,
            **kwargs,
        }
        response = self._client.request(
            method="POST",
            path="comments/setModerationStatus",
            params=params,
        )
        if response.ok:
            return True
        self._client.parse_response(response=response)

    def delete(
        self,
        comment_id: str,
        **kwargs,
    ) -> bool:
        """Deletes a comment.

        Args:
            comment_id:
                ID for the target comment.
            **kwargs:
                Additional parameters for system parameters.
                Refer: https://cloud.google.com/apis/docs/system-parameters.

        Returns:
            Comment delete status.

        """
        params = {"id": comment_id, **kwargs}
        response = self._client.request(
            method="DELETE",
            path="comments",
            params=params,
        )
        if response.ok:
            return True
        self._client.parse_response(response=response)
