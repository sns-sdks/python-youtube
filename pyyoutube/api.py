"""
    Main Api implementation.
"""

from typing import Optional, List, Union

import requests
from requests.models import Response
from requests_oauthlib.oauth2_session import OAuth2Session

from pyyoutube.error import ErrorCode, ErrorMessage, PyYouTubeException
from pyyoutube.models import (
    AccessToken,
    UserProfile,
    ChannelListResponse,
    PlaylistListResponse,
    PlaylistItemListResponse,
    VideoListResponse,
    CommentThreadListResponse,
    CommentListResponse,
    GuideCategoryListResponse,
    VideoCategoryListResponse,
)
from pyyoutube.utils.params_checker import enf_comma_separated, enf_parts


class Api(object):
    """
    Example usage:
        To create an instance of pyyoutube.Api class:

            >>> import pyyoutube
            >>> api = pyyoutube.Api(api_key="your api key")

        To get one channel info:

            >>> res = api.get_channel_info(channel_name="googledevelopers")
            >>> print(res.items[0])

        Now this api provide methods as follows:
            >>> api.get_authorization_url()
            >>> api.exchange_code_to_access_token()
            >>> api.refresh_token()
            >>> api.get_channel_info()
            >>> api.get_playlist_by_id()
            >>> api.get_playlists()
            >>> api.get_playlist_item_by_id()
            >>> api.get_playlist_items()
            >>> api.get_video_by_id()
            >>> api.get_videos_by_chart()
            >>> api.get_videos_by_myrating()
            >>> api.get_comment_thread_by_id()
            >>> api.get_comment_threads()
            >>> api.get_comment_by_id()
            >>> api.get_comments()
            >>> api.get_guide_categories()
            >>> api.get_video_categories()
    """

    BASE_URL = "https://www.googleapis.com/youtube/v3/"
    AUTHORIZATION_URL = "https://accounts.google.com/o/oauth2/v2/auth"
    EXCHANGE_ACCESS_TOKEN_URL = "https://www.googleapis.com/oauth2/v4/token"
    USER_INFO_URL = "https://www.googleapis.com/oauth2/v1/userinfo"

    DEFAULT_REDIRECT_URI = "https://localhost/"

    DEFAULT_SCOPE = [
        "https://www.googleapis.com/auth/youtube",
        "https://www.googleapis.com/auth/userinfo.profile",
    ]

    DEFAULT_STATE = "PyYouTube"
    DEFAULT_TIMEOUT = 10
    DEFAULT_QUOTA = 10000  # this quota reset at 00:00:00(GMT-7) every day.

    def __init__(
        self,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        api_key: Optional[str] = None,
        access_token: Optional[str] = None,
        oauth_redirect_uri: Optional[str] = None,
        timeout: Optional[int] = None,
        proxies: Optional[dict] = None,
        quota: Optional[int] = None,
    ) -> None:
        """
        This Api provide two method to work. Use api key or use access token.

        Args:
            client_id(str, optional):
                Your google app's ID.
            client_secret (str, optional):
                Your google app's secret.
            api_key(str, optional):
                The api key which you create from google api console.
            access_token(str, optional):
                If you not provide api key, you can do authorization to get an access token.
                If all api key and access token provided. Use access token first.
            oauth_redirect_uri(str, optional)
                Determines how Google's authorization server sends a response to your app.
                If not provide will use default https://localhost/
            timeout(int, optional):
                The request timeout.
            proxies(dict, optional):
                If you want use proxy, need point this param.
                param style like requests lib style.
                Refer https://2.python-requests.org//en/latest/user/advanced/#proxies
            quota(int, optional):
                if your key has more quota. you can point this. Default is 10000

        Returns:
            YouTube Api instance.
        """
        self._client_id = client_id
        self._client_secret = client_secret
        self._api_key = api_key
        self._access_token = access_token
        self._refresh_token = None  # This keep current user's refresh token.
        self.oauth_redirect_uri = oauth_redirect_uri or self.DEFAULT_REDIRECT_URI
        self._timeout = timeout
        self.session = requests.Session()
        self.scope = None
        self.proxies = proxies

        self.quota = quota
        if self.quota is None:
            self.quota = self.DEFAULT_QUOTA

        if not (
            (self._client_id and self._client_secret)
            or self._api_key
            or self._access_token
        ):
            raise PyYouTubeException(
                ErrorMessage(
                    status_code=ErrorCode.MISSING_PARAMS,
                    message="Must specify either client key info or api key.",
                )
            )

        if self._timeout is None:
            self._timeout = self.DEFAULT_TIMEOUT

    def get_authorization_url(
        self, scope: Optional[List[str]] = None, **kwargs
    ) -> (str, str):
        """
        Build authorization url to do authorize.

        Args:
            scope (list, optional)
                The scope you want give permission.
                If you not provide, will use default scope.
            kwargs(dict, optional)
                Some other params you want provide.

        Returns:
            The uri you can open on browser to do authorize.
        """

        self.scope = scope
        if self.scope is None:
            self.scope = self.DEFAULT_SCOPE

        session = OAuth2Session(
            client_id=self._client_id,
            scope=self.scope,
            redirect_uri=self.oauth_redirect_uri,
            state=self.DEFAULT_STATE,
        )
        authorization_url, state = session.authorization_url(
            self.AUTHORIZATION_URL,
            access_type="offline",
            prompt="select_account",
            **kwargs,
        )

        return authorization_url, state

    def exchange_code_to_access_token(
        self, authorization_response: str, return_json: bool = False
    ) -> Union[dict, AccessToken]:
        """
        Use the google auth response to get access token

        Args:
            authorization_response (str)
                The response url which google redirect.
            return_json(bool, optional)
                The return data type. If you set True JSON data will be returned.
                False will return pyyoutube.AccessToken

        Return:
            Retrieved access token's info,  pyyoutube.AccessToken instance.
        """

        session = OAuth2Session(
            client_id=self._client_id,
            redirect_uri=self.oauth_redirect_uri,
            state=self.DEFAULT_STATE,
        )
        token = session.fetch_token(
            self.EXCHANGE_ACCESS_TOKEN_URL,
            client_secret=self._client_secret,
            authorization_response=authorization_response,
        )
        self._access_token = session.access_token
        self._refresh_token = session.token["refresh_token"]
        if return_json:
            return token
        else:
            return AccessToken.from_dict(token)

    def refresh_token(
        self, refresh_token: Optional[str] = None, return_json: bool = False
    ) -> Union[dict, AccessToken]:
        """
        Refresh token by api return refresh token.

        Args:
            refresh_token (str)
                The refresh token which the api returns.
            return_json (bool, optional):
                If True JSON data will be returned, instead of pyyoutube.AccessToken
        Return:
            Retrieved new access token's info,  pyyoutube.AccessToken instance.
        """
        if refresh_token is None:
            refresh_token = self._refresh_token
        if refresh_token is None:
            raise PyYouTubeException(
                ErrorMessage(
                    status_code=ErrorCode.MISSING_PARAMS,
                    message=f"Must provide the refresh token or api has been authorized.",
                )
            )

        session = OAuth2Session(client_id=self._client_id)
        auth = {
            "client_id": self._client_id,
            "client_secret": self._client_secret,
        }
        new_token = session.refresh_token(
            self.EXCHANGE_ACCESS_TOKEN_URL, refresh_token=refresh_token, **auth
        )
        self._access_token = session.access_token
        if return_json:
            return new_token
        else:
            return AccessToken.from_dict(new_token)

    @staticmethod
    def _parse_response(response: Response) -> dict:
        """
        Parse response data and check whether errors exists.

        Args:
            response (Response)
                The response which the request return.
        Return:
             response's data
        """
        data = response.json()
        if "error" in data:
            raise PyYouTubeException(response)
        return data

    @staticmethod
    def _parse_data(data: Optional[dict]) -> Union[dict, list]:
        """
        Parse resp data.

        Args:
            data (dict)
                The response data by response.json()
        Return:
             response's items
        """
        items = data["items"]
        return items

    def _request(
        self, resource, method=None, args=None, post_args=None, enforce_auth=True
    ) -> Response:
        """
        Main request sender.

        Args:
            resource(str)
                Resource field is which type data you want to retrieve.
                Such as channels，videos and so on.
            method(str, optional)
                The method this request to send request.
                Default is 'GET'
            args(dict, optional)
                The url params for this request.
            post_args(dict, optional)
                The Post params for this request.
            enforce_auth(bool, optional)
                Whether use google credentials
        Returns:
            response
        """
        if method is None:
            method = "GET"

        if args is None:
            args = dict()

        if post_args is not None:
            method = "POST"

        key = None
        access_token = None
        if self._api_key is not None:
            key = "key"
            access_token = self._api_key
        if self._access_token is not None:
            key = "access_token"
            access_token = self._access_token
        if access_token is None and enforce_auth:
            raise PyYouTubeException(
                ErrorMessage(
                    status_code=ErrorCode.MISSING_PARAMS,
                    message="You must provide your credentials.",
                )
            )

        if enforce_auth:
            if method == "POST" and key not in post_args:
                post_args[key] = access_token
            elif method == "GET" and key not in args:
                args[key] = access_token

        try:
            response = self.session.request(
                method=method,
                url=self.BASE_URL + resource,
                timeout=self._timeout,
                params=args,
                data=post_args,
                proxies=self.proxies,
            )
        except requests.HTTPError as e:
            raise PyYouTubeException(
                ErrorMessage(status_code=ErrorCode.HTTP_ERROR, message=e.args[0])
            )
        else:
            return response

    def get_profile(
        self, access_token: Optional[str] = None, return_json: Optional[bool] = False
    ) -> Union[dict, UserProfile]:
        """
        Get token user info.

        Args:
            access_token(str, optional)
                user access token. If not provide, use api instance access token
            return_json(bool, optional)
                The return data type. If you set True JSON data will be returned.
                False will return pyyoutube.UserProfile

        Returns:
            The data for you given access token's user info.
        """
        if access_token is None:
            access_token = self._access_token
        if access_token is None:
            raise PyYouTubeException(
                ErrorMessage(
                    status_code=ErrorCode.MISSING_PARAMS,
                    message=f"Must provide the access token or api has been authorized.",
                )
            )
        try:
            response = self.session.get(
                self.USER_INFO_URL,
                params={"access_token": access_token},
                timeout=self._timeout,
                proxies=self.proxies,
            )
        except requests.HTTPError as e:
            raise PyYouTubeException(
                ErrorMessage(status_code=ErrorCode.HTTP_ERROR, message=e.args[0])
            )
        data = self._parse_response(response)
        if return_json:
            return data
        else:
            return UserProfile.from_dict(data)

    def paged_by_page_token(
        self, resource: str, args: dict, page_token: Optional[str] = None
    ):
        """
        Response paged by response's page token. If not provide response token

        Args:
            resource (str)
                The resource string need to retrieve data.
            args (dict)
                The args for api.
            page_token (str, optional)
                If token is None, this request is first (not have paged info.)
        Returns:
            Data api origin response.
        """
        if page_token is not None:
            args["pageToken"] = page_token

        resp = self._request(resource=resource, method="GET", args=args)
        data = self._parse_response(resp)  # origin response
        # set page token
        next_page_token = data.get("nextPageToken")
        prev_page_token = data.get("prevPageToken")
        return prev_page_token, next_page_token, data

    def get_channel_info(
        self,
        *,
        channel_id: Optional[Union[str, list, tuple, set]] = None,
        channel_name: Optional[str] = None,
        mine: Optional[bool] = None,
        parts: Optional[Union[str, list, tuple, set]] = None,
        hl: str = "en_US",
        return_json: Optional[bool] = False,
    ):
        """
        Retrieve channel data from YouTube Data API.

        Note:
            1. Don't know why, but now you could't get channel list by given an guide category.
               You can only get list by parameters mine,forUsername,id.
               Refer: https://developers.google.com/youtube/v3/guides/implementation/channels
            2. The origin maxResult param not work for these filter method.

        Args:
            channel_id ((str,list,tuple,set), optional):
                The id or comma-separated id string for youtube channel which you want to get.
                You can also pass this with an id list, tuple, set.
            channel_name (str, optional):
                The name for youtube channel which you want to get.
            mine (bool, optional):
                If you have give the authorization. Will return your channels.
                Must provide the access token.
            parts (str, optional):
                Comma-separated list of one or more channel resource properties.
                If not provided. will use default public properties.
            hl (str, optional):
                If provide this. Will return channel's language localized info.
                This value need https://developers.google.com/youtube/v3/docs/i18nLanguages.
            return_json(bool, optional):
                The return data type. If you set True JSON data will be returned.
                False will return a pyyoutube.ChannelListResponse instance.
        Returns:
            ChannelListResponse instance or original data.
        """

        args = {
            "part": enf_parts(resource="channels", value=parts),
            "hl": hl,
        }
        if channel_name is not None:
            args["forUsername"] = channel_name
        elif channel_id is not None:
            args["id"] = enf_comma_separated("channel_id", channel_id)
        elif mine is not None:
            args["mine"] = mine
        else:
            raise PyYouTubeException(
                ErrorMessage(
                    status_code=ErrorCode.MISSING_PARAMS,
                    message=f"Specify at least one of channel_id,channel_name or mine",
                )
            )

        resp = self._request(resource="channels", method="GET", args=args)

        data = self._parse_response(resp)
        if return_json:
            return data
        else:
            return ChannelListResponse.from_dict(data)

    def get_playlist_by_id(
        self,
        *,
        playlist_id: Union[str, list, tuple, set],
        parts: Optional[Union[str, list, tuple, set]] = None,
        hl: Optional[str] = "en_US",
        return_json: Optional[bool] = False,
    ):
        """
        Retrieve playlist data by given playlist id.

        Args:
            playlist_id ((str,list,tuple,set)):
                The id for playlist that you want to retrieve data.
                You can pass this with single id str,comma-separated id str, or list, tuple, set of id str.
            parts (str, optional):
                Comma-separated list of one or more playlist resource properties.
                You can also pass this with list, tuple, set of part str.
                If not provided. will use default public properties.
            hl (str, optional):
                If provide this. Will return playlist's language localized info.
                This value need https://developers.google.com/youtube/v3/docs/i18nLanguages.
            return_json(bool, optional):
                The return data type. If you set True JSON data will be returned.
                False will return a pyyoutube.PlaylistListResponse instance
        Returns:
            PlaylistListResponse or original data
        """
        args = {
            "id": enf_comma_separated("playlist_id", playlist_id),
            "part": enf_parts(resource="playlists", value=parts),
            "hl": hl,
        }

        resp = self._request(resource="playlists", method="GET", args=args)
        data = self._parse_response(resp)

        if return_json:
            return data
        else:
            return PlaylistListResponse.from_dict(data)

    def get_playlists(
        self,
        *,
        channel_id: Optional[str] = None,
        mine: Optional[bool] = None,
        parts: Optional[Union[str, list, tuple, set]] = None,
        count: Optional[int] = 5,
        limit: Optional[int] = 5,
        hl: Optional[str] = "en_US",
        return_json: Optional[bool] = False,
    ):
        """
        Retrieve channel playlists info from youtube data api.

        Args:
            channel_id (str, optional):
                If provide channel id, this will return pointed channel's playlist info.
            mine (bool, optional):
                If you have given the authorization. Will return your playlists.
                Must provide the access token.
            parts (str, optional):
                Comma-separated list of one or more playlist resource properties.
                You can also pass this with list, tuple, set of part str.
                If not provided. will use default public properties.
            count (int, optional):
                The count will retrieve playlist data.
                Default is 5.
            limit (int, optional):
                The maximum number of items each request to retrieve.
                For playlist, this should not be more than 50.
                Default is 5
            hl (str, optional):
                If provide this. Will return playlist's language localized info.
                This value need https://developers.google.com/youtube/v3/docs/i18nLanguages.
            return_json(bool, optional):
                The return data type. If you set True JSON data will be returned.
                False will return a pyyoutube.PlaylistListResponse instance.
        Returns:
            PlaylistListResponse or original data
        """

        args = {
            "part": enf_parts(resource="playlists", value=parts),
            "hl": hl,
            "maxResults": min(count, limit),
        }

        if channel_id is not None:
            args["channelId"] = channel_id
        elif mine is not None:
            args["mine"] = mine
        else:
            raise PyYouTubeException(
                ErrorMessage(
                    status_code=ErrorCode.MISSING_PARAMS,
                    message=f"Specify at least one of channel_id,playlist_id or mine",
                )
            )

        res_data: Optional[dict] = None
        current_items: List[dict] = []
        next_page_token: Optional[str] = None
        now_items_count: int = 0
        while True:
            prev_page_token, next_page_token, data = self.paged_by_page_token(
                resource="playlists", args=args, page_token=next_page_token,
            )
            items = self._parse_data(data)
            current_items.extend(items)
            now_items_count += len(items)
            if res_data is None:
                res_data = data
            if next_page_token is None:
                break
            if now_items_count >= count:
                break
        res_data["items"] = current_items[:count]
        if return_json:
            return res_data
        else:
            return PlaylistListResponse.from_dict(res_data)

    def get_playlist_item_by_id(
        self,
        *,
        playlist_item_id: Union[str, list, tuple, set],
        parts: Optional[Union[str, list, tuple, set]] = None,
        return_json: Optional[bool] = False,
    ):
        """
        Retrieve playlist Items info by your given id

        Args:
            playlist_item_id ((str,list,tuple,set)):
                The id for playlist item that you want to retrieve info.
                You can pass this with single id str, comma-separated id str.
                Or a list,tuple,set of ids.
            parts ((str,list,tuple,set) optional):
                The resource parts for you want to retrieve.
                If not provide, use default public parts.
                You can pass this with single part str, comma-separated parts str or a list,tuple,set of parts.
            return_json(bool, optional):
                The return data type. If you set True JSON data will be returned.
                False will return a pyyoutube.PlayListItemApiResponse instance.
        Returns:
            PlaylistItemListResponse or original data
        """

        args = {
            "id": enf_comma_separated("playlist_item_id", playlist_item_id),
            "part": enf_parts(resource="playlistItems", value=parts),
        }

        resp = self._request(resource="playlistItems", method="GET", args=args)
        data = self._parse_response(resp)

        if return_json:
            return data
        else:
            return PlaylistItemListResponse.from_dict(data)

    def get_playlist_items(
        self,
        *,
        playlist_id: str,
        parts: Optional[Union[str, list, tuple, set]] = None,
        video_id: Optional[str] = None,
        count: Optional[int] = 5,
        limit: Optional[int] = 5,
        return_json: Optional[bool] = False,
    ):
        """
        Retrieve playlist Items info by your given playlist id

        Args:
            playlist_id (str):
                The id for playlist that you want to retrieve items data.
            parts ((str,list,tuple,set) optional):
                The resource parts for you want to retrieve.
                If not provide, use default public parts.
                You can pass this with single part str, comma-separated parts str or a list,tuple,set of parts.
            video_id (str, Optional):
                Specifies that the request should return only the playlist items that contain the specified video.
            count (int, optional):
                The count will retrieve playlist items data.
                Default is 5.
            limit (int, optional):
                The maximum number of items each request retrieve.
                For playlistItem, this should not be more than 50.
                Default is 5
            return_json(bool, optional):
                The return data type. If you set True JSON data will be returned.
                False will return a pyyoutube.PlayListItemApiResponse instance.
        Returns:
            PlaylistItemListResponse or original data
        """

        args = {
            "playlistId": playlist_id,
            "part": enf_parts(resource="playlistItems", value=parts),
            "maxResults": min(count, limit),
        }
        if video_id is not None:
            args["videoId"] = video_id

        res_data: Optional[dict] = None
        current_items: List[dict] = []
        next_page_token: Optional[str] = None
        now_items_count: int = 0
        while True:
            prev_page_token, next_page_token, data = self.paged_by_page_token(
                resource="playlistItems", args=args, page_token=next_page_token,
            )
            items = self._parse_data(data)
            current_items.extend(items)
            now_items_count += len(items)
            if res_data is None:
                res_data = data
            if next_page_token is None:
                break
            if now_items_count >= count:
                break
        res_data["items"] = current_items[:count]
        if return_json:
            return res_data
        else:
            return PlaylistItemListResponse.from_dict(res_data)

    def get_video_by_id(
        self,
        *,
        video_id: Union[str, list, tuple, set],
        parts: Optional[Union[str, list, tuple, set]] = None,
        hl: Optional[str] = "en_US",
        max_height: Optional[int] = None,
        max_width: Optional[int] = None,
        return_json: Optional[bool] = False,
    ):
        """
        Retrieve video data by given video id.

        Args:
            video_id ((str,list,tuple,set)):
                The id for video that you want to retrieve data.
                You can pass this with single id str, comma-separated id str, or a list,tuple,set of ids.
            parts ((str,list,tuple,set), optional):
                The resource parts for you want to retrieve.
                If not provide, use default public parts.
                You can pass this with single part str, comma-separated parts str or a list,tuple,set of parts.
            hl (str, optional):
                If provide this. Will return video's language localized info.
                This value need https://developers.google.com/youtube/v3/docs/i18nLanguages.
            max_height (int, optional):
                Specifies the maximum height of the embedded player returned in the player.embedHtml property.
                Acceptable values are 72 to 8192, inclusive.
            max_width (int, optional):
                Specifies the maximum width of the embedded player returned in the player.embedHtml property.
                Acceptable values are 72 to 8192, inclusive.
                If provide max_height at the same time. This will may be shorter than max_height.
                For more https://developers.google.com/youtube/v3/docs/videos/list#parameters.
            return_json(bool, optional):
                The return data type. If you set True JSON data will be returned.
                False will return a pyyoutube.VideoListResponse instance.

        Returns:
            VideoListResponse or original data
        """

        args = {
            "id": enf_comma_separated(field="video_id", value=video_id),
            "part": enf_parts(resource="videos", value=parts),
            "hl": hl,
        }
        if max_height is not None:
            args["maxHeight"] = max_height
        if max_width is not None:
            args["maxWidth"] = max_width

        resp = self._request(resource="videos", method="GET", args=args)
        data = self._parse_response(resp)

        if return_json:
            return data
        else:
            return VideoListResponse.from_dict(data)

    def get_videos_by_chart(
        self,
        *,
        chart: str,
        parts: Optional[Union[str, list, tuple, set]] = None,
        hl: Optional[str] = "en_US",
        max_height: Optional[int] = None,
        max_width: Optional[int] = None,
        region_code: Optional[str] = None,
        category_id: Optional[str] = "0",
        count: Optional[int] = 5,
        limit: Optional[int] = 5,
        return_json: Optional[bool] = False,
    ):
        """
        Retrieve a list of YouTube's most popular videos.

        Args:
            chart (str):
                The chart string for you want to retrieve data.
                Acceptable values are: mostPopular
            parts ((str,list,tuple,set), optional):
                The resource parts for you want to retrieve.
                If not provide, use default public parts.
                You can pass this with single part str, comma-separated parts str or a list,tuple,set of parts.
            hl (str, optional):
                If provide this. Will return playlist's language localized info.
                This value need https://developers.google.com/youtube/v3/docs/i18nLanguages.
            max_height (int, optional):
                Specifies the maximum height of the embedded player returned in the player.embedHtml property.
                Acceptable values are 72 to 8192, inclusive.
            max_width (int, optional):
                Specifies the maximum width of the embedded player returned in the player.embedHtml property.
                Acceptable values are 72 to 8192, inclusive.
                If provide max_height at the same time. This will may be shorter than max_height.
                For more https://developers.google.com/youtube/v3/docs/videos/list#parameters.
            region_code (str, optional):
                This parameter instructs the API to select a video chart available in the specified region.
                Value is an ISO 3166-1 alpha-2 country code.
            category_id (str, optional):
                The id for video category that you want to filter.
                Default is 0.
            count (int, optional):
                The count will retrieve videos data.
                Default is 5.
            limit (int, optional):
                The maximum number of items each request retrieve.
                For videos, this should not be more than 50.
                Default is 5
            return_json(bool, optional):
                The return data type. If you set True JSON data will be returned.
                False will return a pyyoutube.PlaylistListResponse instance.

        Returns:
            VideoListResponse or original data
        """
        args = {
            "chart": chart,
            "part": enf_parts(resource="videos", value=parts),
            "hl": hl,
            "maxResults": min(count, limit),
            "videoCategoryId": category_id,
        }
        if max_height is not None:
            args["maxHeight"] = max_height
        if max_width is not None:
            args["maxWidth"] = max_width
        if region_code:
            args["regionCode"] = region_code

        res_data: Optional[dict] = None
        current_items: List[dict] = []
        next_page_token: Optional[str] = None
        now_items_count: int = 0
        while True:
            prev_page_token, next_page_token, data = self.paged_by_page_token(
                resource="videos", args=args, page_token=next_page_token,
            )
            items = self._parse_data(data)
            current_items.extend(items)
            now_items_count += len(items)
            if res_data is None:
                res_data = data
            if next_page_token is None:
                break
            if now_items_count >= count:
                break
        res_data["items"] = current_items[:count]
        if return_json:
            return res_data
        else:
            return VideoListResponse.from_dict(res_data)

    def get_videos_by_myrating(
        self,
        *,
        rating: str,
        parts: Optional[Union[str, list, tuple, set]] = None,
        hl: Optional[str] = "en_US",
        max_height: Optional[int] = None,
        max_width: Optional[int] = None,
        count: Optional[int] = 5,
        limit: Optional[int] = 5,
        return_json: Optional[bool] = False,
    ):
        """
        Retrieve video data by my ration.

        Args:
            rating (str):
                The rating string for you to retrieve data.
                Acceptable values are: dislike, like
            parts ((str,list,tuple,set), optional):
                The resource parts for you want to retrieve.
                If not provide, use default public parts.
                You can pass this with single part str, comma-separated parts str or a list,tuple,set of parts.
            hl (str, optional):
                If provide this. Will return video's language localized info.
                This value need https://developers.google.com/youtube/v3/docs/i18nLanguages.
            max_height (int, optional):
                Specifies the maximum height of the embedded player returned in the player.embedHtml property.
                Acceptable values are 72 to 8192, inclusive.
            max_width (int, optional):
                Specifies the maximum width of the embedded player returned in the player.embedHtml property.
                Acceptable values are 72 to 8192, inclusive.
                If provide max_height at the same time. This will may be shorter than max_height.
                For more https://developers.google.com/youtube/v3/docs/videos/list#parameters.
            count (int, optional):
                The count will retrieve videos data.
                Default is 5.
            limit (int, optional):
                The maximum number of items each request retrieve.
                For videos, this should not be more than 50.
                Default is 5
            return_json(bool, optional):
                The return data type. If you set True JSON data will be returned.
                False will return a pyyoutube.VideoListResponse instance.
        Returns:
            VideoListResponse or original data
        """

        if self._access_token is None:
            raise PyYouTubeException(
                ErrorMessage(
                    status_code=ErrorCode.NEED_AUTHORIZATION,
                    message="This method can only used with authorization",
                )
            )
        args = {
            "myRating": rating,
            "part": enf_parts(resource="videos", value=parts),
            "hl": hl,
            "maxResults": min(count, limit),
        }

        if max_height is not None:
            args["maxHeight"] = max_height
        if max_width is not None:
            args["maxWidth"] = max_width

        res_data: Optional[dict] = None
        current_items: List[dict] = []
        next_page_token: Optional[str] = None
        now_items_count: int = 0
        while True:
            prev_page_token, next_page_token, data = self.paged_by_page_token(
                resource="videos", args=args, page_token=next_page_token,
            )
            items = self._parse_data(data)
            current_items.extend(items)
            now_items_count += len(items)
            if res_data is None:
                res_data = data
            if next_page_token is None:
                break
            if now_items_count >= count:
                break
        res_data["items"] = current_items[:count]
        if return_json:
            return res_data
        else:
            return VideoListResponse.from_dict(res_data)

    def get_comment_thread_by_id(
        self,
        *,
        comment_thread_id: Union[str, list, tuple, set],
        parts: Optional[Union[str, list, tuple, set]] = None,
        text_format: Optional[str] = "html",
        return_json: Optional[bool] = False,
    ):
        """
        Retrieve the comment thread info by given id.

        Args:
            comment_thread_id ((str,list,tuple,set)):
                The id for comment thread that you want to retrieve data.
                You can pass this with single id str, comma-separated id str, or a list,tuple,set of ids.
            parts ((str,list,tuple,set), optional):
                The resource parts for you want to retrieve.
                If not provide, use default public parts.
                You can pass this with single part str, comma-separated parts str or a list,tuple,set of parts.
            text_format (str, optional):
                Comments left by users format style.
                Acceptable values are: html, plainText.
                Default is html.
            return_json(bool, optional):
                The return data type. If you set True JSON data will be returned.
                False will return a pyyoutube.CommentThreadListResponse instance.
        Returns:
            CommentThreadListResponse or original data
        """

        args = {
            "id": enf_comma_separated("comment_thread_id", comment_thread_id),
            "part": enf_parts(resource="commentThreads", value=parts),
            "textFormat": text_format,
        }

        resp = self._request(resource="commentThreads", method="GET", args=args)
        data = self._parse_response(resp)

        if return_json:
            return data
        else:
            return CommentThreadListResponse.from_dict(data)

    def get_comment_threads(
        self,
        *,
        all_to_channel_id: Optional[str] = None,
        channel_id: Optional[str] = None,
        video_id: Optional[str] = None,
        parts: Optional[Union[str, list, tuple, set]] = None,
        moderation_status: Optional[str] = None,
        order: Optional[str] = None,
        search_terms: Optional[str] = None,
        text_format: Optional[str] = "html",
        count: Optional[int] = 20,
        limit: Optional[int] = 20,
        return_json: Optional[bool] = False,
    ):
        """
        Retrieve the comment threads info by given filter condition.

        Args:
            all_to_channel_id (str, optional):
                If you provide this with a channel id, will return all comment threads associated with the channel.
                The response can include comments about the channel or about the channel's videos.
            channel_id (str, optional):
                If you provide this with a channel id, will return the comment threads associated with the channel.
                But the response not include comments about the channel's videos.
            video_id  (str, optional):
                If you provide this with a video id, will return the comment threads associated with the video.
            parts ((str,list,tuple,set), optional)
                The resource parts for you want to retrieve.
                If not provide, use default public parts.
                You can pass this with single part str, comma-separated parts str or a list,tuple,set of parts.
            moderation_status (str, optional):
                This parameter must used with authorization.
                If you provide this. the response will return comment threads match this filter only.
                Acceptable values are:
                    - heldForReview: Retrieve comment threads that are awaiting review by a moderator.
                    - likelySpam: Retrieve comment threads classified as likely to be spam.
                    - published: Retrieve threads of published comments. this is default for all.
                See more: https://developers.google.com/youtube/v3/docs/commentThreads/list#parameters
            order (str, optional):
                Order parameter specifies the order in which the API response should list comment threads.
                Acceptable values are:
                    - time: Comment threads are ordered by time. This is the default behavior.
                    - relevance: Comment threads are ordered by relevance.
            search_terms (str, optional):
                The searchTerms parameter instructs the API to limit the API response to only contain comments
                that contain the specified search terms.
            text_format (str, optional):
                Comments left by users format style.
                Acceptable values are: html, plainText.
                Default is html.
            count (int, optional):
                The count will retrieve comment threads data.
                Default is 20.
            limit (int, optional):
                The maximum number of items each request retrieve.
                For comment threads, this should not be more than 100.
                Default is 20.
            return_json(bool, optional):
                The return data type. If you set True JSON data will be returned.
                False will return a pyyoutube.CommentThreadListResponse instance.

        Returns:
            CommentThreadListResponse or original data
        """

        args = {
            "part": enf_parts(resource="commentThreads", value=parts),
            "maxResults": min(count, limit),
            "textFormat": text_format,
        }

        if all_to_channel_id:
            args["allThreadsRelatedToChannelId"] = (all_to_channel_id,)
        elif channel_id:
            args["channelId"] = channel_id
        elif video_id:
            args["videoId"] = video_id
        else:
            raise PyYouTubeException(
                ErrorMessage(
                    status_code=ErrorCode.MISSING_PARAMS,
                    message=f"Specify at least one of all_to_channel_id, channel_id or video_id",
                )
            )

        if moderation_status:
            args["moderationStatus"] = moderation_status
        if order:
            args["order"] = order
        if search_terms:
            args["searchTerms"] = search_terms

        res_data: Optional[dict] = None
        current_items: List[dict] = []
        next_page_token: Optional[str] = None
        now_items_count: int = 0
        while True:
            prev_page_token, next_page_token, data = self.paged_by_page_token(
                resource="commentThreads", args=args, page_token=next_page_token,
            )
            items = self._parse_data(data)
            current_items.extend(items)
            now_items_count += len(items)
            if res_data is None:
                res_data = data
            if next_page_token is None:
                break
            if now_items_count >= count:
                break
        res_data["items"] = current_items[:count]
        if return_json:
            return res_data
        else:
            return CommentThreadListResponse.from_dict(res_data)

    def get_comment_by_id(
        self,
        *,
        comment_id: Union[str, list, tuple, set],
        parts: Optional[Union[str, list, tuple, set]] = None,
        text_format: Optional[str] = "html",
        return_json: Optional[bool] = False,
    ):
        """
        Retrieve comment info by given comment id str.

        Args:
            comment_id (str, optional):
                The id for comment that you want to retrieve data.
                You can pass this with single id str, comma-separated id str, or a list,tuple,set of ids.
            parts ((str,list,tuple,set), optional):
                The resource parts for you want to retrieve.
                If not provide, use default public parts.
                You can pass this with single part str, comma-separated parts str or a list,tuple,set of parts.
            text_format (str, optional):
                Comments left by users format style.
                Acceptable values are: html, plainText.
                Default is html.
            return_json(bool, optional):
                The return data type. If you set True JSON data will be returned.
                False will return a pyyoutube.CommentListResponse instance.

        Returns:
            CommentListResponse or original data
        """

        args = {
            "id": enf_comma_separated(field="comment_id", value=comment_id),
            "part": enf_parts(resource="comments", value=parts),
            "textFormat": text_format,
        }

        resp = self._request(resource="comments", method="GET", args=args)
        data = self._parse_response(resp)

        if return_json:
            return data
        else:
            return CommentListResponse.from_dict(data)

    def get_comments(
        self,
        *,
        parent_id: str,
        parts: Optional[Union[str, list, tuple, set]] = None,
        text_format: Optional[str] = "html",
        count: Optional[int] = 20,
        limit: Optional[int] = 20,
        return_json: Optional[bool] = False,
    ):
        """
        Retrieve comments info by given parent id.
        Note: YouTube currently supports replies only for top-level comments.
        However, replies to replies may be supported in the future.

        Args:
            parent_id (str):
                Provide the ID of the comment for which replies should be retrieved.
            parts ((str,list,tuple,set), optional):
                The resource parts for you want to retrieve.
                If not provide, use default public parts.
                You can pass this with single part str, comma-separated parts str or a list,tuple,set of parts.
            text_format (str, optional):
                Comments left by users format style.
                Acceptable values are: html, plainText.
                Default is html.
            count (int, optional):
                The count will retrieve videos data.
                Default is 20.
            limit (int, optional):
                The maximum number of items each request retrieve.
                For comments, this should not be more than 100.
                Default is 20.
            return_json(bool, optional):
                The return data type. If you set True JSON data will be returned.
                False will return a pyyoutube.CommentListResponse instance.
        Returns:
            CommentListResponse or original data
        """

        args = {
            "parentId": parent_id,
            "part": enf_parts(resource="comments", value=parts),
            "textFormat": text_format,
            "maxResults": min(count, limit),
        }

        res_data: Optional[dict] = None
        current_items: List[dict] = []
        next_page_token: Optional[str] = None
        now_items_count: int = 0
        while True:
            prev_page_token, next_page_token, data = self.paged_by_page_token(
                resource="comments", args=args, page_token=next_page_token,
            )
            items = self._parse_data(data)
            current_items.extend(items)
            now_items_count += len(items)
            if res_data is None:
                res_data = data
            if next_page_token is None:
                break
            if now_items_count >= count:
                break
        res_data["items"] = current_items[:count]
        if return_json:
            return res_data
        else:
            return CommentListResponse.from_dict(res_data)

    def _get_categories(
        self,
        *,
        resource: str,
        category_id: Optional[Union[str, list, tuple, set]] = None,
        region_code: Optional[str] = None,
        parts: Optional[Union[str, list, tuple, set]] = None,
        hl: Optional[str] = "en_US",
        return_json: Optional[bool] = False,
    ):
        """
        This is the base method for get guide or video categories.

        Args:
            resource (str):
                The category resource type.
                 Acceptable values are: guideCategories, videoCategories.
        Returns:
            Model instance or original data.
        """

        if resource == "guideCategories":
            data_model = GuideCategoryListResponse
        elif resource == "videoCategories":
            data_model = VideoCategoryListResponse
        else:
            raise PyYouTubeException(
                ErrorMessage(
                    status_code=ErrorCode.INVALID_PARAMS,
                    message="Parameter resource only accept for guideCategories or videoCategories",
                )
            )

        args = {
            "part": enf_parts(resource=resource, value=parts),
            "hl": hl,
        }

        if category_id is not None:
            args["id"] = enf_comma_separated(field="category_id", value=category_id)
        elif region_code is not None:
            args["regionCode"] = region_code
        else:
            raise PyYouTubeException(
                ErrorMessage(
                    status_code=ErrorCode.MISSING_PARAMS,
                    message="Specify at least one of category_id or region_code",
                )
            )

        resp = self._request(resource=resource, method="GET", args=args)
        data = self._parse_response(resp)

        if return_json:
            return data
        else:
            return data_model.from_dict(data)

    def get_guide_categories(
        self,
        *,
        category_id: Optional[Union[str, list, tuple, set]] = None,
        region_code: Optional[str] = None,
        parts: Optional[Union[str, list, tuple, set]] = None,
        hl: Optional[str] = "en_US",
        return_json: Optional[bool] = False,
    ):
        """
        Retrieve guide categories by category id or region code.

        Args:
            category_id ((str,list,tuple,set), optional):
                The id for guide category thread that you want to retrieve data.
                You can pass this with single id str, comma-separated id str, or a list,tuple,set of ids.
            region_code (str, optional):
                The region code that you want to retrieve guide categories.
                The parameter value is an ISO 3166-1 alpha-2 country code.
                Refer: https://www.iso.org/iso-3166-country-codes.html
            parts ((str,list,tuple,set) optional):
                The resource parts for you want to retrieve.
                If not provide, use default public parts.
                You can pass this with single part str, comma-separated parts str or a list,tuple,set of parts.
            hl (str, optional):
                If provide this. Will return guide category's language localized info.
                This value need https://developers.google.com/youtube/v3/docs/i18nLanguages.
                Default is en_US.
            return_json(bool, optional):
                The return data type. If you set True JSON data will be returned.
                False will return a pyyoutube.GuideCategoryListResponse instance.
        Returns:
            GuideCategoryListResponse or original data
        """

        return self._get_categories(
            resource="guideCategories",
            category_id=category_id,
            region_code=region_code,
            parts=parts,
            hl=hl,
            return_json=return_json,
        )

    def get_video_categories(
        self,
        *,
        category_id: Optional[Union[str, list, tuple, set]] = None,
        region_code: Optional[str] = None,
        parts: Optional[Union[str, list, tuple, set]] = None,
        hl: Optional[str] = "en_US",
        return_json: Optional[bool] = False,
    ):
        """
        Retrieve video categories by category id or region code.

        Args:
            category_id ((str,list,tuple,set), optional):
                The id for video category thread that you want to retrieve data.
                You can pass this with single id str, comma-separated id str, or a list,tuple,set of ids.
            region_code (str, optional):
                The region code that you want to retrieve guide categories.
                The parameter value is an ISO 3166-1 alpha-2 country code.
                Refer: https://www.iso.org/iso-3166-country-codes.html
            parts ((str,list,tuple,set) optional):
                The resource parts for you want to retrieve.
                If not provide, use default public parts.
                You can pass this with single part str, comma-separated parts str or a list,tuple,set of parts.
            hl (str, optional):
                If provide this. Will return video category's language localized info.
                This value need https://developers.google.com/youtube/v3/docs/i18nLanguages.
                Default is en_US.
            return_json(bool, optional):
                The return data type. If you set True JSON data will be returned.
                False will return a pyyoutube.VideoCategoryListResponse instance.
        Returns:
            VideoCategoryListResponse or original data
        """
        return self._get_categories(
            resource="videoCategories",
            category_id=category_id,
            region_code=region_code,
            parts=parts,
            hl=hl,
            return_json=return_json,
        )
