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
)
from pyyoutube.utils.params_checker import enf_comma_separated, enf_parts


class Api(object):
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
    def _parse_response(
        response: Response
    ) -> dict:
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
            2. The origin maxResult param not work.

        Args:
            channel_id (str, optional)
                The id or comma-separated id string for youtube channel which you want to get.
                You can also pass this with an id list, tuple, set.
            channel_name (str, optional)
                The name for youtube channel which you want to get.
            mine (bool, optional)
                If you have give the authorization. Will return your channels.
                Must provide the access token.
            parts (str, optional)
                Comma-separated list of one or more channel resource properties.
                If not provided. will use default public properties.
            hl (str, optional)
                If provide this. Will return channel's language localized info.
                This value need https://developers.google.com/youtube/v3/docs/i18nLanguages.
            return_json(bool, optional)
                The return data type. If you set True JSON data will be returned.
                False will return pyyoutube.Channel
        Returns:
            The data for you given channel.
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
        playlist_id: Optional[Union[str, list, tuple, set]] = None,
        parts: Optional[Union[str, list, tuple, set]] = None,
        hl: Optional[str] = "en_US",
        return_json: Optional[bool] = False,
    ):
        """
        Retrieve playlist data by given playlist id.

        Args:
            playlist_id (str optional)
                If provide this. will return those playlist's info.
                You can pass this with single id str,comma-separated id str,
                or list, tuple, set of id str.
            parts (str, optional)
                Comma-separated list of one or more playlist resource properties.
                You can also pass this with list, tuple, set of part str.
                If not provided. will use default public properties.
            hl (str, optional)
                If provide this. Will return playlist's language localized info.
                This value need https://developers.google.com/youtube/v3/docs/i18nLanguages.
            return_json(bool, optional)
                The return data type. If you set True JSON data will be returned.
                False will return pyyoutube.PlayList
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
            channel_id (str, optional)
                If provide channel id, this will return pointed channel's playlist info.
            mine (bool, optional)
                If you have give the authorization. Will return your playlists.
                Must provide the access token.
            parts (str, optional)
                Comma-separated list of one or more playlist resource properties.
                You can also pass this with list, tuple, set of part str.
                If not provided. will use default public properties.
            count (int, optional)
                The count will retrieve playlist data.
                Default is 5.
            limit (int, optional)
                The maximum number of items each request to retrieve.
                For playlist, this should not be more than 50.
                Default is 5
            hl (str, optional)
                If provide this. Will return playlist's language localized info.
                This value need https://developers.google.com/youtube/v3/docs/i18nLanguages.
            return_json(bool, optional)
                The return data type. If you set True JSON data will be returned.
                False will return pyyoutube.PlayList
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
