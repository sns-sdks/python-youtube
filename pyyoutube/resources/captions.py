"""
    Captions resource implementation
"""
from typing import Optional, Union

from requests import Response

from pyyoutube.resources.base_resource import Resource
from pyyoutube.media import Media, MediaUpload
from pyyoutube.models import Caption, CaptionListResponse
from pyyoutube.utils.params_checker import enf_comma_separated, enf_parts


class CaptionsResource(Resource):
    """A caption resource represents a YouTube caption track

    References: https://developers.google.com/youtube/v3/docs/captions
    """

    def list(
        self,
        parts: Optional[Union[str, list, tuple, set]] = None,
        video_id: Optional[str] = None,
        caption_id: Optional[Union[str, list, tuple, set]] = None,
        on_behalf_of_content_owner: Optional[str] = None,
        return_json: bool = False,
        **kwargs: Optional[dict],
    ) -> Union[dict, CaptionListResponse]:
        """Returns a list of caption tracks that are associated with a specified video.

        Args:
            parts:
                Comma-separated list of one or more caption resource properties.
            video_id:
                The parameter specifies the YouTube video ID of the video for which the API
                should return caption tracks.
            caption_id:
                The id parameter specifies a comma-separated list of IDs that identify the
                caption resources that should be retrieved.
            on_behalf_of_content_owner:
                This parameter can only be used in a properly authorized request.
                Note: This parameter is intended exclusively for YouTube content partners.
            return_json:
                Type for returned data. If you set True JSON data will be returned.
            kwargs:
                Additional parameters for system parameters.
                Refer: https://cloud.google.com/apis/docs/system-parameters.

        Returns:
            Caption data
        """

        params = {
            "part": enf_parts(resource="captions", value=parts),
            "videoId": video_id,
            "id": enf_comma_separated(field="caption_id", value=caption_id),
            "onBehalfOfContentOwner": on_behalf_of_content_owner,
            **kwargs,
        }
        response = self._client.request(path="captions", params=params)
        data = self._client.parse_response(response=response)
        return data if return_json else CaptionListResponse.from_dict(data)

    def insert(
        self,
        body: Union[dict, Caption],
        media: Media,
        parts: Optional[Union[str, list, tuple, set]] = None,
        on_behalf_of_content_owner: Optional[str] = None,
        sync: Optional[bool] = None,
        **kwargs,
    ) -> MediaUpload:
        """Uploads a caption track.

        Args:
            body:
                Provide caption data in the request body. You can give dataclass or just a dict with data.
            media:
                Caption media data to upload.
            parts:
                The part parameter specifies the caption resource parts that
                the API response will include. Set the parameter value to snippet.
            on_behalf_of_content_owner:
                This parameter can only be used in a properly authorized request.
                Note: This parameter is intended exclusively for YouTube content partners.
            sync:
                The sync parameter indicates whether YouTube should automatically synchronize the caption
                file with the audio track of the video.
                If you set the value to true, YouTube will disregard any time codes that are in the uploaded
                caption file and generate new time codes for the captions.
            **kwargs:
                Additional parameters for system parameters.
                Refer: https://cloud.google.com/apis/docs/system-parameters.

        Returns:
            Caption data.
        """

        params = {
            "part": enf_parts(resource="captions", value=parts),
            "onBehalfOfContentOwner": on_behalf_of_content_owner,
            "sync": sync,
            **kwargs,
        }
        # Build a media upload instance.
        media_upload = MediaUpload(
            client=self._client,
            resource="captions",
            media=media,
            params=params,
            body=body.to_dict_ignore_none(),
        )
        return media_upload

    def update(
        self,
        body: Union[dict, Caption],
        media: Optional[Media] = None,
        parts: Optional[Union[str, list, tuple, set]] = None,
        on_behalf_of_content_owner: Optional[str] = None,
        sync: Optional[bool] = None,
        return_json: bool = False,
        **kwargs,
    ) -> Union[dict, Caption, MediaUpload]:
        """Updates a caption track.

        Args:
            body:
                Provide caption data in the request body. You can give dataclass or just a dict with data.
            media:
                New caption media.
            parts:
                The part parameter specifies the caption resource parts that
                the API response will include. Set the parameter value to snippet.
            on_behalf_of_content_owner:
                This parameter can only be used in a properly authorized request.
                Note: This parameter is intended exclusively for YouTube content partners.
            sync:
                The sync parameter indicates whether YouTube should automatically synchronize the caption
                file with the audio track of the video.
                If you set the value to true, YouTube will disregard any time codes that are in the uploaded
                caption file and generate new time codes for the captions.
            return_json:
                Type for returned data. If you set True JSON data will be returned.
            **kwargs:
                Additional parameters for system parameters.
                Refer: https://cloud.google.com/apis/docs/system-parameters.
        Returns:
            Caption data.

        """
        params = {
            "part": enf_parts(resource="captions", value=parts),
            "onBehalfOfContentOwner": on_behalf_of_content_owner,
            "sync": sync,
            **kwargs,
        }
        if media is not None:
            # Build a media upload instance.
            media_upload = MediaUpload(
                client=self._client,
                resource="captions",
                media=media,
                params=params,
                body=body.to_dict_ignore_none(),
            )
            return media_upload

        response = self._client.request(
            method="PUT",
            path="captions",
            params=params,
            json=body,
        )
        data = self._client.parse_response(response=response)
        return data if return_json else Caption.from_dict(data)

    def download(
        self,
        caption_id: str,
        on_behalf_of_content_owner: Optional[str] = None,
        tfmt: Optional[str] = None,
        tlang: Optional[str] = None,
        **kwargs,
    ) -> Response:
        """Downloads a caption track.

        Args:
            caption_id:
                ID for the caption track that is being deleted.
            on_behalf_of_content_owner:
                This parameter can only be used in a properly authorized request.
                Note: This parameter is intended exclusively for YouTube content partners.
            tfmt:
                Specifies that the caption track should be returned in a specific format.
                Supported values are:
                    sbv – SubViewer subtitle
                    scc – Scenarist Closed Caption format
                    srt – SubRip subtitle
                    ttml – Timed Text Markup Language caption
                    vtt – Web Video Text Tracks caption
            tlang:
                Specifies that the API response should return a translation of the specified caption track.
            **kwargs:
                Additional parameters for system parameters.
                Refer: https://cloud.google.com/apis/docs/system-parameters.

        Returns:
            Response form YouTube.
        """
        params = {
            "id": caption_id,
            "onBehalfOfContentOwner": on_behalf_of_content_owner,
            "tfmt": tfmt,
            "tlang": tlang,
            **kwargs,
        }
        response = self._client.request(
            path=f"captions/{caption_id}",
            params=params,
        )
        return response

    def delete(
        self,
        caption_id: str,
        on_behalf_of_content_owner: Optional[str] = None,
        **kwargs,
    ) -> bool:
        """Deletes a specified caption track.

        Args:
            caption_id:
                ID for the caption track that is being deleted.
            on_behalf_of_content_owner:
                This parameter can only be used in a properly authorized request.
                Note: This parameter is intended exclusively for YouTube content partners.
            **kwargs:
                Additional parameters for system parameters.
                Refer: https://cloud.google.com/apis/docs/system-parameters.

        Returns:
            Delete status

        Raises:
            PyYouTubeException: Request not success.
        """
        params = {
            "id": caption_id,
            "onBehalfOfContentOwner": on_behalf_of_content_owner,
            **kwargs,
        }

        response = self._client.request(path="captions", method="DELETE", params=params)
        if response.ok:
            return True
        self._client.parse_response(response=response)
