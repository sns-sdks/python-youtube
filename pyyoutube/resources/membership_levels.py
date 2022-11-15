"""
    Membership levels resource implementation.
"""
from typing import Optional, Union

from pyyoutube.models import MembershipsLevelListResponse
from pyyoutube.resources.base_resource import Resource
from pyyoutube.utils.params_checker import enf_parts


class MembershipLevelsResource(Resource):
    """A membershipsLevel resource identifies a pricing level managed by the creator that authorized the API request.

    References: https://developers.google.com/youtube/v3/docs/membershipsLevels
    """

    def list(
        self,
        parts: Optional[Union[str, list, tuple, set]] = None,
        return_json: bool = False,
        **kwargs: Optional[dict],
    ) -> Union[dict, MembershipsLevelListResponse]:
        """Lists membership levels for the channel that authorized the request.

        Args:
            parts:
                Comma-separated list of one or more channel resource properties.
                Accepted values: id,snippet
            return_json:
                Type for returned data. If you set True JSON data will be returned.
            **kwargs:
                Additional parameters for system parameters.
                Refer: https://cloud.google.com/apis/docs/system-parameters.

        Returns:
            Membership levels data.

        """
        params = {
            "part": enf_parts(resource="membershipsLevels", value=parts),
            **kwargs,
        }
        response = self._client.request(path="membershipsLevels", params=params)
        data = self._client.parse_response(response=response)
        return data if return_json else MembershipsLevelListResponse.from_dict(data)
