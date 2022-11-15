"""
    Members resource implementation.
"""

from typing import Optional, Union

from pyyoutube.resources.base_resource import Resource
from pyyoutube.models import MemberListResponse
from pyyoutube.utils.params_checker import enf_parts, enf_comma_separated


class MembersResource(Resource):
    """A member resource represents a channel member for a YouTube channel.

    References: https://developers.google.com/youtube/v3/docs/members
    """

    def list(
        self,
        parts: Optional[Union[str, list, tuple, set]] = None,
        mode: Optional[str] = None,
        max_results: Optional[int] = None,
        page_token: Optional[str] = None,
        has_access_to_level: Optional[str] = None,
        filter_by_member_channel_id: Optional[Union[str, list, tuple, set]] = None,
        return_json: bool = False,
        **kwargs: Optional[dict],
    ) -> Union[dict, MemberListResponse]:
        """Lists members (formerly known as "sponsors") for a channel.

        Args:
            parts:
                Comma-separated list of one or more channel resource properties.
                Accepted values: snippet
            mode:
                Indicates which members will be included in the API response.
                Accepted values:
                    - all_current: List current members, from newest to oldest.
                    - updates: List only members that joined or upgraded since the previous API call.
            max_results:
                The parameter specifies the maximum number of items that should be returned
                the result set.
                Acceptable values are 0 to 1000, inclusive. The default value is 5.
            page_token:
                The parameter identifies a specific page in the result set that should be returned.
            has_access_to_level:
                A level ID that specifies the minimum level that members in the result set should have.
            filter_by_member_channel_id:
                specifies a comma-separated list of channel IDs that can be used to check the membership
                status of specific users.
                Maximum of 100 channels can be specified per call.
            return_json:
                Type for returned data. If you set True JSON data will be returned.
            **kwargs:
                Additional parameters for system parameters.
                Refer: https://cloud.google.com/apis/docs/system-parameters.

        Returns:
            Members data.
        """

        params = {
            "part": enf_parts(resource="members", value=parts),
            "mode": mode,
            "maxResults": max_results,
            "pageToken": page_token,
            "hasAccessToLevel": has_access_to_level,
            "filterByMemberChannelId": enf_comma_separated(
                field="filter_by_member_channel_id", value=filter_by_member_channel_id
            ),
            **kwargs,
        }
        response = self._client.request(path="members", params=params)
        data = self._client.parse_response(response=response)
        return data if return_json else MemberListResponse.from_dict(data)
