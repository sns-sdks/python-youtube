"""
    Video abuse report reasons resource implementation.
"""
from typing import Optional, Union

from pyyoutube.resources.base_resource import Resource
from pyyoutube.models import VideoAbuseReportReasonListResponse
from pyyoutube.utils.params_checker import enf_parts


class VideoAbuseReportReasonsResource(Resource):
    """A videoAbuseReportReason resource contains information about a reason that a video would be flagged
    for containing abusive content.

    References: https://developers.google.com/youtube/v3/docs/videoAbuseReportReasons
    """

    def list(
        self,
        parts: Optional[Union[str, list, tuple, set]] = None,
        hl: Optional[str] = None,
        return_json: bool = False,
        **kwargs: Optional[dict],
    ) -> Union[dict, VideoAbuseReportReasonListResponse]:
        """Retrieve a list of reasons that can be used to report abusive videos.

        Args:
            parts:
                Comma-separated list of one or more channel resource properties.
                Accepted values: id,snippet
            hl:
                Specifies the language that should be used for text values in the API response.
                The default value is en_US.
            return_json:
                Type for returned data. If you set True JSON data will be returned.
            **kwargs:
                Additional parameters for system parameters.
                Refer: https://cloud.google.com/apis/docs/system-parameters.

        Returns:
            reasons data.
        """
        params = {
            "part": enf_parts(resource="videoAbuseReportReasons", value=parts),
            "hl": hl,
            **kwargs,
        }
        response = self._client.request(path="videoAbuseReportReasons", params=params)
        data = self._client.parse_response(response=response)
        return (
            data if return_json else VideoAbuseReportReasonListResponse.from_dict(data)
        )
