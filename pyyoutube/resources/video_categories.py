"""
    Video categories resource implementation.
"""

from typing import Optional, Union

from pyyoutube.error import PyYouTubeException, ErrorMessage, ErrorCode
from pyyoutube.resources.base_resource import Resource
from pyyoutube.models import VideoCategoryListResponse
from pyyoutube.utils.params_checker import enf_comma_separated, enf_parts


class VideoCategoriesResource(Resource):
    """A videoCategory resource identifies a category that has been or could be associated with uploaded videos.

    References: https://developers.google.com/youtube/v3/docs/videoCategories
    """

    def list(
        self,
        parts: Optional[Union[str, list, tuple, set]] = None,
        category_id: Optional[Union[str, list, tuple, set]] = None,
        region_code: Optional[str] = None,
        hl: Optional[str] = None,
        return_json: bool = False,
        **kwargs: Optional[dict],
    ) -> Union[dict, VideoCategoryListResponse]:
        """Returns a list of categories that can be associated with YouTube videos.

        Args:
            parts:
                Comma-separated list of one or more video category resource properties.
                Accepted values: snippet
            category_id:
                Specifies a comma-separated list of video category IDs for the resources that you are retrieving.
            region_code:
                Instructs the API to return the list of video categories available in the specified country.
                The parameter value is an ISO 3166-1 alpha-2 country code.
            hl:
                Specifies the language that should be used for text values in the API response.
                The default value is en_US.
            return_json:
                Type for returned data. If you set True JSON data will be returned.
            **kwargs:
                Additional parameters for system parameters.
                Refer: https://cloud.google.com/apis/docs/system-parameters.

        Returns:
            Video category data.
        Raises:
            PyYouTubeException: Missing filter parameter.
        """
        params = {
            "part": enf_parts(resource="videoCategories", value=parts),
            "hl": hl,
            **kwargs,
        }

        if category_id is not None:
            params["id"] = enf_comma_separated(field="category_id", value=category_id)
        elif region_code is not None:
            params["regionCode"] = region_code
        else:
            raise PyYouTubeException(
                ErrorMessage(
                    status_code=ErrorCode.MISSING_PARAMS,
                    message=f"Specify at least one of category_id or region_code",
                )
            )
        response = self._client.request(path="videoCategories", params=params)
        data = self._client.parse_response(response=response)
        return data if return_json else VideoCategoryListResponse.from_dict(data)
