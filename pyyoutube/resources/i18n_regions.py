"""
    i18n regions resource implementation.
"""

from typing import Optional, Union

from pyyoutube.resources.base_resource import Resource
from pyyoutube.models import I18nRegionListResponse
from pyyoutube.utils.params_checker import enf_parts


class I18nRegionsResource(Resource):
    """An i18nRegion resource identifies a geographic area that a YouTube user can select as
    the preferred content region.

    References: https://developers.google.com/youtube/v3/docs/i18nRegions
    """

    def list(
        self,
        parts: Optional[Union[str, list, tuple, set]] = None,
        hl: Optional[str] = None,
        return_json: bool = False,
        **kwargs: Optional[dict],
    ) -> Union[dict, I18nRegionListResponse]:
        """Returns a list of content regions that the YouTube website supports.

        Args:
            parts:
                Comma-separated list of one or more i18n regions resource properties.
                Accepted values: snippet.
            hl:
                Specifies the language that should be used for text values in the API response.
                The default value is en_US.
            return_json:
                Type for returned data. If you set True JSON data will be returned.
            **kwargs:
                Additional parameters for system parameters.
                Refer: https://cloud.google.com/apis/docs/system-parameters.

        Returns:
            i18n regions data.
        """
        params = {
            "part": enf_parts(resource="i18nRegions", value=parts),
            "hl": hl,
            **kwargs,
        }
        response = self._client.request(path="i18nRegions", params=params)
        data = self._client.parse_response(response=response)
        return data if return_json else I18nRegionListResponse.from_dict(data)
