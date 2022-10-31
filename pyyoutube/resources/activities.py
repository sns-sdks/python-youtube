"""
    Activities resource implementation
"""
from typing import Optional, Union

from pyyoutube.error import PyYouTubeException, ErrorMessage, ErrorCode
from pyyoutube.resources.base_resource import Resource
from pyyoutube.models import ActivityListResponse
from pyyoutube.utils.params_checker import enf_parts


class ActivitiesResource(Resource):
    """An activity resource contains information about an action that a particular channel,
    or user, has taken on YouTube.

    References: https://developers.google.com/youtube/v3/docs/activities
    """

    def list(
        self,
        parts: Optional[Union[str, list, tuple, set]] = None,
        channel_id: Optional[str] = None,
        mine: Optional[bool] = None,
        max_results: Optional[int] = None,
        page_token: Optional[str] = None,
        published_after: Optional[str] = None,
        published_before: Optional[str] = None,
        region_code: Optional[str] = None,
        return_json: bool = False,
        **kwargs,
    ) -> Union[dict, ActivityListResponse]:
        """Returns a list of channel activity events that match the request criteria.

        Args:
            parts:
                Comma-separated list of one or more activity resource properties.
            channel_id:
                The channelId parameter specifies a unique YouTube channel ID.
            mine:
                This parameter can only be used in a properly authorized request. Set this parameter's value
                to true to retrieve a feed of the authenticated user's activities.
            max_results:
                The parameter specifies the maximum number of items that should be returned
                the result set.
                Acceptable values are 0 to 50, inclusive. The default value is 5.
            page_token:
                The parameter identifies a specific page in the result set that should be returned.
            published_after:
                The parameter specifies the earliest date and time that an activity could
                have occurred for that activity to be included in the API response.
            published_before:
                The parameter specifies the date and time before which an activity must
                have occurred for that activity to be included in the API response.
            region_code:
                The parameter instructs the API to return results for the specified country.
            return_json:
                Type for returned data. If you set True JSON data will be returned.
            kwargs:
                Additional parameters for system parameters.
                Refer: https://cloud.google.com/apis/docs/system-parameters.

        Returns:
            Activities data

        """
        params = {
            "part": enf_parts(resource="activities", value=parts),
            "maxResults": max_results,
            "pageToken": page_token,
            "publishedAfter": published_after,
            "publishedBefore": published_before,
            "regionCode": region_code,
            **kwargs,
        }
        if channel_id is not None:
            params["channelId"] = channel_id
        elif mine is not None:
            params["mine"] = mine
        else:
            raise PyYouTubeException(
                ErrorMessage(
                    status_code=ErrorCode.MISSING_PARAMS,
                    message=f"Specify at least one of for_username, id, managedByMe or mine",
                )
            )

        response = self._client.request(path="activities", params=params)
        data = self._client.parse_response(response=response)
        return data if return_json else ActivityListResponse.from_dict(data)
