"""
    Main Api implementation.
"""

from typing import Optional, List, Union

import requests
from requests.auth import HTTPBasicAuth
from requests.models import Response
from requests_oauthlib.oauth2_session import OAuth2Session

from pyyoutube.error import ErrorCode, ErrorMessage, PyYouTubeException
from pyyoutube.models import (
    AccessToken,
    UserProfile,
    ActivityListResponse,
    CaptionListResponse,
    ChannelListResponse,
    ChannelSectionResponse,
    PlaylistListResponse,
    PlaylistItemListResponse,
    VideoListResponse,
    CommentThreadListResponse,
    CommentListResponse,
    VideoCategoryListResponse,
    SearchListResponse,
    SubscriptionListResponse,
    I18nRegionListResponse,
    I18nLanguageListResponse,
    MemberListResponse,
    MembershipsLevelListResponse,
    VideoAbuseReportReasonListResponse,
)
from pyyoutube.utils.params_checker import enf_comma_separated, enf_parts


class Api(object):
    """
    Example usage:
        To create an instance of pyyoutube.Api class:

            >>> import pyyoutube
            >>> api = pyyoutube.Api(api_key="your api key")

        To get one channel info:

            >>> res = api.get_channel_info(channel_id="UC_x5XG1OV2P6uZZ5FSM9Ttw")
            >>> print(res.items[0])

        Now this api provide methods as follows:
            >>> api.get_authorization_url()
            >>> api.generate_access_token()
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
            >>> api.get_video_categories()
            >>> api.get_subscription_by_id()
            >>> api.get_subscription_by_channel()
            >>> api.get_subscription_by_me()
            >>> api.get_activities_by_channel()
            >>> api.get_activities_by_me()
            >>> api.get_captions_by_video()
            >>> api.get_channel_sections_by_id()
            >>> api.get_channel_sections_by_channel()
            >>> api.get_i18n_regions()
            >>> api.get_i18n_languages()
            >>> api.get_video_abuse_report_reason()
            >>> api.search()
            >>> api.search_by_keywords()
            >>> api.search_by_developer()
            >>> api.search_by_mine()
            >>> api.search_by_related_video()
    """

    BASE_URL = "https://www.googleapis.com/youtube/v3/"
    AUTHORIZATION_URL = "https://accounts.google.com/o/oauth2/v2/auth"
    EXCHANGE_ACCESS_TOKEN_URL = "https://oauth2.googleapis.com/token"
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
        timeout: Optional[int] = None,
        proxies: Optional[dict] = None,
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
            timeout(int, optional):
                The request timeout.
            proxies(dict, optional):
                If you want use proxy, need point this param.
                param style like requests lib style.
                Refer https://2.python-requests.org//en/latest/user/advanced/#proxies

        Returns:
            YouTube Api instance.
        """
        self._client_id = client_id
        self._client_secret = client_secret
        self._api_key = api_key
        self._access_token = access_token
        self._refresh_token = None  # This keep current user's refresh token.
        self._timeout = timeout
        self.session = requests.Session()
        self.proxies = proxies

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

    def _get_oauth_session(
        self,
        redirect_uri: Optional[str] = None,
        scope: Optional[List[str]] = None,
        **kwargs,
    ) -> OAuth2Session:
        """
        Build a request session for OAuth.

        Args:
            redirect_uri(str, optional)
                Determines how Google's authorization server sends a response to your app.
                If not provide will use default https://localhost/
            scope (list, optional)
                The scope you want give permission.
                If you not provide, will use default scope.
            kwargs(dict, optional)
                Some other params you want provide.

        Returns:
            OAuth2 Session
        """
        if redirect_uri is None:
            redirect_uri = self.DEFAULT_REDIRECT_URI

        if scope is None:
            scope = self.DEFAULT_SCOPE

        return OAuth2Session(
            client_id=self._client_id,
            scope=scope,
            redirect_uri=redirect_uri,
            state=self.DEFAULT_STATE,
            **kwargs,
        )

    def get_authorization_url(
        self,
        redirect_uri: Optional[str] = None,
        scope: Optional[List[str]] = None,
        **kwargs,
    ) -> (str, str):
        """
        Build authorization url to do authorize.

        Args:
            redirect_uri(str, optional)
                Determines how Google's authorization server sends a response to your app.
                If not provide will use default https://localhost/
            scope (list, optional)
                The scope you want give permission.
                If you not provide, will use default scope.
            kwargs(dict, optional)
                Some other params you want provide.

        Returns:
            The uri you can open on browser to do authorize.
        """
        oauth_session = self._get_oauth_session(
            redirect_uri=redirect_uri,
            scope=scope,
            **kwargs,
        )
        authorization_url, state = oauth_session.authorization_url(
            self.AUTHORIZATION_URL,
            access_type="offline",
            prompt="select_account",
            **kwargs,
        )

        return authorization_url, state

    def generate_access_token(
        self,
        authorization_response: str,
        redirect_uri: Optional[str] = None,
        scope: Optional[List[str]] = None,
        return_json: bool = False,
        **kwargs,
    ) -> Union[dict, AccessToken]:
        """
        Use the google auth response to get access token

        Args:
            authorization_response (str)
                The response url which google redirect.
            redirect_uri(str, optional)
                Determines how Google's authorization server sends a response to your app.
                If not provide will use default https://localhost/
            scope (list, optional)
                The scope you want give permission.
                If you not provide, will use default scope.
            return_json(bool, optional)
                The return data type. If you set True JSON data will be returned.
                False will return pyyoutube.AccessToken
            kwargs(dict, optional)
                Some other params you want provide.
        Return:
            Retrieved access token's info, pyyoutube.AccessToken instance.
        """

        oauth_session = self._get_oauth_session(
            redirect_uri=redirect_uri,
            scope=scope,
            **kwargs,
        )
        token = oauth_session.fetch_token(
            self.EXCHANGE_ACCESS_TOKEN_URL,
            client_secret=self._client_secret,
            authorization_response=authorization_response,
            proxies=self.proxies,
        )
        self._access_token = oauth_session.access_token
        self._refresh_token = oauth_session.token["refresh_token"]
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

        refresh_token = refresh_token if refresh_token else self._refresh_token

        if refresh_token is None:
            raise PyYouTubeException(
                ErrorMessage(
                    status_code=ErrorCode.MISSING_PARAMS,
                    message=f"Must provide the refresh token or api has been authorized.",
                )
            )

        oauth_session = OAuth2Session(client_id=self._client_id)
        auth = HTTPBasicAuth(self._client_id, self._client_secret)
        new_token = oauth_session.refresh_token(
            self.EXCHANGE_ACCESS_TOKEN_URL,
            refresh_token=refresh_token,
            auth=auth,
        )
        self._access_token = oauth_session.access_token
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
        self,
        resource: str,
        args: dict,
        count: Optional[int] = None,
    ):
        """
        Response paged by response's page token. If not provide response token

        Args:
            resource (str):
                The resource string need to retrieve data.
            args (dict)
                The args for api.
            count (int, optional):
                The count for result items you want to get.
                If provide this with None, will retrieve all items.
                Note:
                    The all items maybe too much. Notice your app's cost.
        Returns:
            Data api origin response.
        """
        res_data: Optional[dict] = None
        current_items: List[dict] = []
        page_token: Optional[str] = None
        now_items_count: int = 0

        while True:
            if page_token is not None:
                args["pageToken"] = page_token

            resp = self._request(resource=resource, method="GET", args=args)
            data = self._parse_response(resp)  # origin response
            # set page token
            page_token = data.get("nextPageToken")
            prev_page_token = data.get("prevPageToken")

            # parse results.
            items = self._parse_data(data)
            current_items.extend(items)
            now_items_count += len(items)
            if res_data is None:
                res_data = data
            # first check the count if satisfies.
            if count is not None:
                if now_items_count >= count:
                    current_items = current_items[:count]
                    break
            # if have no page token, mean no more data.
            if page_token is None:
                break
        res_data["items"] = current_items

        # use last request page token
        res_data["nextPageToken"] = page_token
        res_data["prevPageToken"] = prev_page_token
        return res_data

    def get_activities_by_channel(
        self,
        *,
        channel_id: str,
        parts: Optional[Union[str, list, tuple, set]] = None,
        before: Optional[str] = None,
        after: Optional[str] = None,
        region_code: Optional[str] = None,
        count: Optional[int] = 20,
        limit: int = 20,
        page_token: Optional[str] = None,
        return_json: bool = False,
    ):
        """
        Retrieve given channel's activities data.

        Args:
            channel_id (str):
                The id for channel which you want to get activities data.
            parts ((str,list,tuple,set) optional):
                The resource parts for activities you want to retrieve.
                If not provide, use default public parts.
                You can pass this with single part str, comma-separated parts str or a list,tuple,set of parts.
            before (str, optional):
                Set this will only return the activities occurred before this timestamp.
                This need specified in ISO 8601 (YYYY-MM-DDThh:mm:ss.sZ) format.
            after (str, optional):
                Set this will only return the activities occurred after this timestamp.
                This need specified in ISO 8601 (YYYY-MM-DDThh:mm:ss.sZ) format.
            region_code (str, optional):
                Set this will only return the activities for the specified country.
                This need specified with an ISO 3166-1 alpha-2 country code.
            count (int, optional):
                The count will retrieve activities data.
                Default is 20.
                If provide this with None, will retrieve all activities.
            limit (int, optional):
                The maximum number of items each request retrieve.
                For activities, this should not be more than 50.
                Default is 20.
            page_token (str, optional):
                The token of the page of activities result to retrieve.
                You can use this retrieve point result page directly.
                And you should know about the page result set for YouTube.
            return_json(bool, optional):
                The return data type. If you set True JSON data will be returned.
                False will return a pyyoutube.ActivityListResponse instance.

        Returns:
            ActivityListResponse or original data.
        """

        if count is None:
            limit = 50  # for activities the max limit for per request is 50
        else:
            limit = min(count, limit)

        args = {
            "channelId": channel_id,
            "part": enf_parts(resource="activities", value=parts),
            "maxResults": limit,
        }

        if before:
            args["publishedBefore"] = before
        if after:
            args["publishedAfter"] = after
        if region_code:
            args["regionCode"] = region_code

        if page_token is not None:
            args["pageToken"] = page_token

        res_data = self.paged_by_page_token(
            resource="activities", args=args, count=count
        )

        if return_json:
            return res_data
        else:
            return ActivityListResponse.from_dict(res_data)

    def get_activities_by_me(
        self,
        *,
        parts: Optional[Union[str, list, tuple, set]] = None,
        before: Optional[str] = None,
        after: Optional[str] = None,
        region_code: Optional[str] = None,
        count: Optional[int] = 20,
        limit: int = 20,
        page_token: Optional[str] = None,
        return_json: bool = False,
    ):
        """
        Retrieve authorized user's activities.

        Note:
            This need you do authorize first.

        Args:
            parts ((str,list,tuple,set) optional):
                The resource parts for activities you want to retrieve.
                If not provide, use default public parts.
                You can pass this with single part str, comma-separated parts str or a list,tuple,set of parts.
            before (str, optional):
                Set this will only return the activities occurred before this timestamp.
                This need specified in ISO 8601 (YYYY-MM-DDThh:mm:ss.sZ) format.
            after (str, optional):
                Set this will only return the activities occurred after this timestamp.
                This need specified in ISO 8601 (YYYY-MM-DDThh:mm:ss.sZ) format.
            region_code (str, optional):
                Set this will only return the activities for the specified country.
                This need specified with an ISO 3166-1 alpha-2 country code.
            count (int, optional):
                The count will retrieve activities data.
                Default is 20.
                If provide this with None, will retrieve all activities.
            limit (int, optional):
                The maximum number of items each request retrieve.
                For activities, this should not be more than 50.
                Default is 20.
            page_token (str, optional):
                The token of the page of activities result to retrieve.
                You can use this retrieve point result page directly.
                And you should know about the page result set for YouTube.
            return_json(bool, optional):
                The return data type. If you set True JSON data will be returned.
                False will return a pyyoutube.ActivityListResponse instance.

        Returns:
            ActivityListResponse or original data.
        """

        if count is None:
            limit = 50  # for activities the max limit for per request is 50
        else:
            limit = min(count, limit)

        args = {
            "mine": True,
            "part": enf_parts(resource="activities", value=parts),
            "maxResults": limit,
        }

        if before:
            args["publishedBefore"] = before
        if after:
            args["publishedAfter"] = after
        if region_code:
            args["regionCode"] = region_code

        if page_token is not None:
            args["pageToken"] = page_token

        res_data = self.paged_by_page_token(
            resource="activities", args=args, count=count
        )

        if return_json:
            return res_data
        else:
            return ActivityListResponse.from_dict(res_data)

    def get_captions_by_video(
        self,
        *,
        video_id: str,
        parts: Optional[Union[str, list, tuple, set]] = None,
        caption_id: Optional[Union[str, list, tuple, set]] = None,
        return_json: bool = False,
    ):
        """
        Retrieve authorized user's video's caption data.

        Note:
            This need you do authorize first.

        Args:
            video_id (str):
                The id for video which you want to get caption.
            parts ((str,list,tuple,set) optional):
                The resource parts for caption you want to retrieve.
                If not provide, use default public parts.
                You can pass this with single part str, comma-separated parts str or a list,tuple,set of parts.
            caption_id ((str,list,tuple,set)):
                The id for caption that you want to get data.
                You can pass this with single id str,comma-separated id str, or list, tuple, set of id str.
            return_json(bool, optional):
                The return data type. If you set True JSON data will be returned.
                False will return a pyyoutube.CaptionListResponse instance.
        Returns:
            CaptionListResponse or original data.
        """

        args = {
            "videoId": video_id,
            "part": enf_parts("captions", parts),
        }

        if caption_id is not None:
            args["id"] = enf_comma_separated("caption_id", caption_id)

        resp = self._request(resource="captions", method="GET", args=args)
        data = self._parse_response(resp)

        if return_json:
            return data
        else:
            return CaptionListResponse.from_dict(data)

    def get_channel_info(
        self,
        *,
        channel_id: Optional[Union[str, list, tuple, set]] = None,
        for_username: Optional[str] = None,
        mine: Optional[bool] = None,
        parts: Optional[Union[str, list, tuple, set]] = None,
        hl: str = "en_US",
        return_json: Optional[bool] = False,
    ):
        """
        Retrieve channel data from YouTube Data API.

        Note:
            1. Don't know why, but now you couldn't get channel list by given an guide category.
               You can only get list by parameters mine,forUsername,id.
               Refer: https://developers.google.com/youtube/v3/guides/implementation/channels
            2. The origin maxResult param not work for these filter method.

        Args:
            channel_id ((str,list,tuple,set), optional):
                The id or comma-separated id string for youtube channel which you want to get.
                You can also pass this with an id list, tuple, set.
            for_username (str, optional):
                The name for YouTube username which you want to get.
                Note: This name may the old youtube version's channel's user's username, Not the the channel name.
                Refer: https://developers.google.com/youtube/v3/guides/working_with_channel_ids
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
        if for_username is not None:
            args["forUsername"] = for_username
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

    def get_channel_sections_by_id(
        self,
        *,
        section_id: Union[str, list, tuple, set],
        parts: Optional[Union[str, list, tuple, set]] = None,
        return_json: Optional[bool] = False,
    ) -> Union[ChannelSectionResponse, dict]:
        """
        Retrieve channel section info by his ids(s).

        Args:
            section_id:
                The id(s) for channel sections.
                You can pass this with single id str, comma-separated id str, or a list,tuple,set of ids.
            parts:
                The resource parts for channel section you want to retrieve.
                If not provide, use default public parts.
                You can pass this with single part str, comma-separated parts str or a list,tuple,set of parts.
            return_json:
                The return data type. If you set True JSON data will be returned.
                False will return a pyyoutube.ChannelSectionResponse instance.
        Returns:
            ChannelSectionResponse or original data.
        """

        args = {
            "id": enf_comma_separated(field="section_id", value=section_id),
            "part": enf_parts(resource="channelSections", value=parts),
        }

        resp = self._request(resource="channelSections", args=args)
        data = self._parse_response(resp)

        if return_json:
            return data
        else:
            return ChannelSectionResponse.from_dict(data)

    def get_channel_sections_by_channel(
        self,
        *,
        channel_id: Optional[str] = None,
        mine: bool = False,
        parts: Optional[Union[str, list, tuple, set]] = None,
        return_json: Optional[bool] = False,
    ) -> Union[ChannelSectionResponse, dict]:
        """
        Retrieve channel sections by channel id.

        Args:
            channel_id:
                The id for channel which you want to get channel sections.
            mine:
                If you want to get your channel's sections, set this with True.
                And this need your authorization.
            parts:
                The resource parts for channel section you want to retrieve.
                If not provide, use default public parts.
                You can pass this with single part str, comma-separated parts str or a list,tuple,set of parts.
            return_json:
                The return data type. If you set True JSON data will be returned.
                False will return a pyyoutube.ChannelSectionResponse instance.
        Returns:
            ChannelSectionResponse or original data.
        """

        args = {
            "part": enf_parts(resource="channelSections", value=parts),
        }

        if mine:
            args["mine"] = mine
        else:
            args["channelId"] = channel_id

        resp = self._request(resource="channelSections", args=args)
        data = self._parse_response(resp)

        if return_json:
            return data
        else:
            return ChannelSectionResponse.from_dict(data)

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
        page_token: Optional[str] = None,
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
                If provide this with None, will retrieve all comments.
            limit (int, optional):
                The maximum number of items each request retrieve.
                For comments, this should not be more than 100.
                Default is 20.
            page_token(str, optional):
                The token of the page of comments result to retrieve.
                You can use this retrieve point result page directly.
                And you should know about the the result set for YouTube.
            return_json(bool, optional):
                The return data type. If you set True JSON data will be returned.
                False will return a pyyoutube.CommentListResponse instance.
        Returns:
            CommentListResponse or original data
        """

        if count is None:
            limit = 100  # for comments the max limit for per request is 100
        else:
            limit = min(count, limit)

        args = {
            "parentId": parent_id,
            "part": enf_parts(resource="comments", value=parts),
            "textFormat": text_format,
            "maxResults": limit,
        }

        if page_token is not None:
            args["pageToken"] = page_token

        res_data = self.paged_by_page_token(resource="comments", args=args, count=count)
        if return_json:
            return res_data
        else:
            return CommentListResponse.from_dict(res_data)

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
        page_token: Optional[str] = None,
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
                If provide this with None, will retrieve all comment threads.
            limit (int, optional):
                The maximum number of items each request retrieve.
                For comment threads, this should not be more than 100.
                Default is 20.
            page_token(str, optional):
                The token of the page of commentThreads result to retrieve.
                You can use this retrieve point result page directly.
                And you should know about the the result set for YouTube.
            return_json(bool, optional):
                The return data type. If you set True JSON data will be returned.
                False will return a pyyoutube.CommentThreadListResponse instance.

        Returns:
            CommentThreadListResponse or original data
        """

        if count is None:
            limit = 100  # for commentThreads the max limit for per request is 100
        else:
            limit = min(count, limit)

        args = {
            "part": enf_parts(resource="commentThreads", value=parts),
            "maxResults": limit,
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

        if page_token is not None:
            args["pageToken"] = page_token

        res_data = self.paged_by_page_token(
            resource="commentThreads", args=args, count=count
        )
        if return_json:
            return res_data
        else:
            return CommentThreadListResponse.from_dict(res_data)

    def get_i18n_languages(
        self,
        *,
        parts: Optional[Union[str, list, tuple, set]] = None,
        hl: Optional[str] = "en_US",
        return_json: Optional[bool] = False,
    ) -> Union[I18nLanguageListResponse, dict]:
        """
        Returns a list of application languages that the YouTube website supports.

        Args:
            parts:
                The resource parts for i18n language you want to retrieve.
                If not provide, use default public parts.
                You can pass this with single part str, comma-separated parts str or a list,tuple,set of parts.
            hl:
                If provide this. Will return i18n language's language localized info.
                This value need https://developers.google.com/youtube/v3/docs/i18nLanguages.
            return_json:
                The return data type. If you set True JSON data will be returned.
                False will return a pyyoutube.I18nLanguageListResponse instance.

        Returns:
            I18nLanguageListResponse or original data.
        """

        args = {"hl": hl, "part": enf_parts(resource="i18nLanguages", value=parts)}

        resp = self._request(resource="i18nLanguages", args=args)
        data = self._parse_response(resp)

        if return_json:
            return data
        else:
            return I18nLanguageListResponse.from_dict(data)

    def get_i18n_regions(
        self,
        *,
        parts: Optional[Union[str, list, tuple, set]] = None,
        hl: Optional[str] = "en_US",
        return_json: Optional[bool] = False,
    ) -> Union[I18nRegionListResponse, dict]:
        """
        Retrieve all available regions.

        Args:
            parts:
                The resource parts for i18n region you want to retrieve.
                If not provide, use default public parts.
                You can pass this with single part str, comma-separated parts str or a list,tuple,set of parts.
            hl:
                If provide this. Will return i18n region's language localized info.
                This value need https://developers.google.com/youtube/v3/docs/i18nLanguages.
            return_json:
                The return data type. If you set True JSON data will be returned.
                False will return a pyyoutube.I18nRegionListResponse instance.
        Returns:
            I18nRegionListResponse or origin data
        """

        args = {"hl": hl, "part": enf_parts(resource="i18nRegions", value=parts)}

        resp = self._request(resource="i18nRegions", args=args)
        data = self._parse_response(resp)

        if return_json:
            return data
        else:
            return I18nRegionListResponse.from_dict(data)

    def get_members(
        self,
        *,
        parts: Optional[Union[str, list, tuple, set]] = None,
        mode: Optional[str] = "all_current",
        count: Optional[int] = 5,
        limit: Optional[int] = 5,
        page_token: Optional[str] = None,
        has_access_to_level: Optional[str] = None,
        filter_by_member_channel_id: Optional[Union[str, list, tuple, set]] = None,
        return_json: Optional[bool] = False,
    ) -> Union[MemberListResponse, dict]:
        """
        Retrieve a list of members for a channel.

        Args:
            parts ((str,list,tuple,set) optional):
                The resource parts for member you want to retrieve.
                If not provide, use default public parts.
                You can pass this with single part str, comma-separated parts str or a list,tuple,set of parts.
            mode:
                The mode parameter indicates which members will be included in the API response.
                Set the parameter value to one of the following values:
                    - all_current (default): List current members, from newest to oldest. When this value is used,
                        the end of the list is reached when the API response does not contain a nextPageToken.
                    - updates : List only members that joined or upgraded since the previous API call.
                        Note: The first call starts a new stream of updates but does not actually return any members.
                        To start retrieving the membership updates, you need to poll the endpoint using the
                        nextPageToken at your desired frequency.
                        Note that when this value is used, the API response always contains a nextPageToken.
            count (int, optional):
                The count will retrieve videos data.
                Default is 5.
            limit (int, optional):
                The maximum number of items each request retrieve.
                For members, this should not be more than 1000.
                Default is 5.
            page_token (str, optional):
                The token of the page of search result to retrieve.
                You can use this retrieve point result page directly.
                And you should know about the the result set for YouTube.
            has_access_to_level (str, optional):
                The hasAccessToLevel parameter value is a level ID that specifies the minimum level
                that members in the result set should have.
            filter_by_member_channel_id ((str,list,tuple,set) optional):
                A list of channel IDs that can be used to check the membership status of specific users.
                A maximum of 100 channels can be specified per call.
            return_json (bool, optional):
                The return data type. If you set True JSON data will be returned.
                False will return a pyyoutube.MemberListResponse instance.
        Returns:
            MemberListResponse or original data
        """

        if count is None:
            limit = 1000
        else:
            limit = min(count, limit)

        args = {
            "part": enf_parts(resource="members", value=parts),
            "maxResults": limit,
        }

        if mode:
            args["mode"] = mode

        if page_token is not None:
            args["pageToken"] = page_token

        if has_access_to_level:
            args["hasAccessToLevel"] = has_access_to_level

        if filter_by_member_channel_id:
            args["filterByMemberChannelId"] = enf_parts(
                resource="filterByMemberChannelId",
                value=filter_by_member_channel_id,
                check=False,
            )

        res_data = self.paged_by_page_token(
            resource="members",
            args=args,
            count=count,
        )
        if return_json:
            return res_data
        else:
            return MemberListResponse.from_dict(res_data)

    def get_membership_levels(
        self,
        *,
        parts: Optional[Union[str, list, tuple, set]] = None,
        return_json: Optional[bool] = False,
    ) -> Union[MembershipsLevelListResponse, dict]:
        """
        Retrieve membership levels for a channel

        Notes:
            This requires your authorization.

        Args:
            parts ((str,list,tuple,set) optional):
                The resource parts for membership level you want to retrieve.
                If not provide, use default public parts.
                You can pass this with single part str, comma-separated parts str or a list,tuple,set of parts.
            return_json (bool, optional):
                The return data type. If you set True JSON data will be returned.
                False will return a pyyoutube.MembershipsLevelListResponse instance.

        Returns:
            MembershipsLevelListResponse or original data
        """

        args = {
            "part": enf_parts(resource="membershipsLevels", value=parts),
        }

        resp = self._request(resource="membershipsLevels", args=args)
        data = self._parse_response(resp)

        if return_json:
            return data
        else:
            return MembershipsLevelListResponse.from_dict(data)

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
        page_token: Optional[str] = None,
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
                If provide this with None, will retrieve all playlist items.
            limit (int, optional):
                The maximum number of items each request retrieve.
                For playlistItem, this should not be more than 50.
                Default is 5
            page_token(str, optional):
                The token of the page of playlist items result to retrieve.
                You can use this retrieve point result page directly.
                And you should know about the the result set for YouTube.
            return_json(bool, optional):
                The return data type. If you set True JSON data will be returned.
                False will return a pyyoutube.PlayListItemApiResponse instance.
        Returns:
            PlaylistItemListResponse or original data
        """

        if count is None:
            limit = 50  # for playlistItems the max limit for per request is 50
        else:
            limit = min(count, limit)

        args = {
            "playlistId": playlist_id,
            "part": enf_parts(resource="playlistItems", value=parts),
            "maxResults": limit,
        }
        if video_id is not None:
            args["videoId"] = video_id

        if page_token is not None:
            args["pageToken"] = page_token

        res_data = self.paged_by_page_token(
            resource="playlistItems", args=args, count=count
        )
        if return_json:
            return res_data
        else:
            return PlaylistItemListResponse.from_dict(res_data)

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
        page_token: Optional[str] = None,
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
                If provide this with None, will retrieve all playlists.
            limit (int, optional):
                The maximum number of items each request to retrieve.
                For playlist, this should not be more than 50.
                Default is 5
            hl (str, optional):
                If provide this. Will return playlist's language localized info.
                This value need https://developers.google.com/youtube/v3/docs/i18nLanguages.
            page_token(str, optional):
                The token of the page of playlists result to retrieve.
                You can use this retrieve point result page directly.
                And you should know about the the result set for YouTube.
            return_json(bool, optional):
                The return data type. If you set True JSON data will be returned.
                False will return a pyyoutube.PlaylistListResponse instance.
        Returns:
            PlaylistListResponse or original data
        """

        if count is None:
            limit = 50  # for playlists the max limit for per request is 50
        else:
            limit = min(count, limit)

        args = {
            "part": enf_parts(resource="playlists", value=parts),
            "hl": hl,
            "maxResults": limit,
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

        if page_token is not None:
            args["pageToken"] = page_token

        res_data = self.paged_by_page_token(
            resource="playlists", args=args, count=count
        )
        if return_json:
            return res_data
        else:
            return PlaylistListResponse.from_dict(res_data)

    def search(
        self,
        *,
        parts: Optional[Union[str, list, tuple, set]] = None,
        for_developer: Optional[bool] = None,
        for_mine: Optional[bool] = None,
        related_to_video_id: Optional[str] = None,
        channel_id: Optional[str] = None,
        channel_type: Optional[str] = None,
        event_type: Optional[str] = None,
        location: Optional[str] = None,
        location_radius: Optional[str] = None,
        count: Optional[int] = 10,
        limit: Optional[int] = 10,
        order: Optional[str] = None,
        published_after: Optional[str] = None,
        published_before: Optional[str] = None,
        q: Optional[str] = None,
        region_code: Optional[str] = None,
        relevance_language: Optional[str] = None,
        safe_search: Optional[str] = None,
        topic_id: Optional[str] = None,
        search_type: Optional[Union[str, list, tuple, set]] = None,
        video_caption: Optional[str] = None,
        video_category_id: Optional[str] = None,
        video_definition: Optional[str] = None,
        video_dimension: Optional[str] = None,
        video_duration: Optional[str] = None,
        video_embeddable: Optional[str] = None,
        video_license: Optional[str] = None,
        video_syndicated: Optional[str] = None,
        video_type: Optional[str] = None,
        page_token: Optional[str] = None,
        return_json: Optional[bool] = False,
    ) -> Union[SearchListResponse, dict]:
        """
        Main search api implementation.
        You can find all parameters description at https://developers.google.com/youtube/v3/docs/search/list#parameters

        Returns:
            SearchListResponse or original data
        """
        parts = enf_parts(resource="search", value=parts)
        if search_type is None:
            search_type = "video,channel,playlist"
        else:
            search_type = enf_comma_separated(field="search_type", value=search_type)

        args = {
            "part": parts,
            "maxResults": min(limit, count),
        }
        if for_developer:
            args["forDeveloper"] = for_developer
        if for_mine:
            args["forMine"] = for_mine
        if related_to_video_id:
            args["relatedToVideoId"] = related_to_video_id
        if channel_id:
            args["channelId"] = channel_id
        if channel_type:
            args["channelType"] = channel_type
        if event_type:
            args["eventType"] = event_type
        if location:
            args["location"] = location
        if location_radius:
            args["locationRadius"] = location_radius
        if order:
            args["order"] = order
        if published_after:
            args["publishedAfter"] = published_after
        if published_before:
            args["publishedBefore"] = published_before
        if q:
            args["q"] = q
        if region_code:
            args["regionCode"] = region_code
        if relevance_language:
            args["relevanceLanguage"] = relevance_language
        if safe_search:
            args["safeSearch"] = safe_search
        if topic_id:
            args["topicId"] = topic_id
        if search_type:
            args["type"] = search_type
        if video_caption:
            args["videoCaption"] = video_caption
        if video_category_id:
            args["videoCategoryId"] = video_category_id
        if video_definition:
            args["videoDefinition"] = video_definition
        if video_dimension:
            args["videoDimension"] = video_dimension
        if video_duration:
            args["videoDuration"] = video_duration
        if video_embeddable:
            args["videoEmbeddable"] = video_embeddable
        if video_license:
            args["videoLicense"] = video_license
        if video_syndicated:
            args["videoSyndicated"] = video_syndicated
        if video_type:
            args["videoType"] = video_type
        if page_token:
            args["pageToken"] = page_token

        res_data = self.paged_by_page_token(resource="search", args=args, count=count)

        if return_json:
            return res_data
        else:
            return SearchListResponse.from_dict(res_data)

    def search_by_keywords(
        self,
        *,
        q: Optional[str],
        parts: Optional[Union[str, list, tuple, set]] = None,
        search_type: Optional[Union[str, list, tuple, set]] = None,
        count: Optional[int] = 25,
        limit: Optional[int] = 25,
        page_token: Optional[str] = None,
        return_json: Optional[bool] = False,
        **kwargs: Optional[dict],
    ) -> Union[SearchListResponse, dict]:
        """
        This is simplest usage for search api. You can only passed the keywords to retrieve data from YouTube.
        And the result will include videos,playlists and channels.

        Note: A call to this method has a quota cost of 100 units.

        Args:
            q (str):
                Your keywords can also use the Boolean NOT (-) and OR (|) operators to exclude videos or
                to find videos that are associated with one of several search terms. For example,
                to search for videos matching either "boating" or "sailing",
                set the q parameter value to boating|sailing. Similarly,
                to search for videos matching either "boating" or "sailing" but not "fishing",
                set the q parameter value to boating|sailing -fishing.
                Note that the pipe character must be URL-escaped when it is sent in your API request.
                The URL-escaped value for the pipe character is %7C.
            parts ((str,list,tuple,set) optional):
                The resource parts for you want to retrieve.
                If not provide, use default public parts.
                You can pass this with single part str, comma-separated parts str or a list,tuple,set of parts.
            search_type ((str,list,tuple,set), optional):
                Parameter restricts a search query to only retrieve a particular type of resource.
                You can pass this with single part str, comma-separated parts str or a list,tuple,set of parts.
                The default value is video,channel,playlist
                Acceptable values are:
                    - channel
                    - playlist
                    - video
            count (int, optional):
                The count will retrieve videos data.
                Default is 25.
            limit (int, optional):
                The maximum number of items each request retrieve.
                For search, this should not be more than 50.
                Default is 25.
            page_token (str, optional):
                The token of the page of search result to retrieve.
                You can use this retrieve point result page directly.
                And you should know about the the result set for YouTube.
            return_json(bool, optional):
                The return data type. If you set True JSON data will be returned.
                False will return a pyyoutube.SearchListResponse instance.
            kwargs:
                If you want use this pass more args. You can use this.

        Returns:
            SearchListResponse or original data
        """
        return self.search(
            parts=parts,
            q=q,
            search_type=search_type,
            count=count,
            limit=limit,
            page_token=page_token,
            return_json=return_json,
            **kwargs,
        )

    def search_by_developer(
        self,
        *,
        parts: Optional[Union[str, list, tuple, set]],
        q: Optional[str] = None,
        count: Optional[int] = 25,
        limit: Optional[int] = 25,
        page_token: Optional[str] = None,
        return_json: Optional[bool] = False,
        **kwargs,
    ) -> Union[SearchListResponse, dict]:
        """
        Parameter restricts the search to only retrieve videos uploaded via the developer's application or website.

        Args:
            parts:
                The resource parts for you want to retrieve.
                If not provide, use default public parts.
                You can pass this with single part str, comma-separated parts str or a list,tuple,set of parts.
            q:
                Your keywords can also use the Boolean NOT (-) and OR (|) operators to exclude videos or
                to find videos that are associated with one of several search terms. For example,
                to search for videos matching either "boating" or "sailing",
                set the q parameter value to boating|sailing. Similarly,
                to search for videos matching either "boating" or "sailing" but not "fishing",
                set the q parameter value to boating|sailing -fishing.
                Note that the pipe character must be URL-escaped when it is sent in your API request.
                The URL-escaped value for the pipe character is %7C.
            count:
                The count will retrieve videos data.
                Default is 25.
            limit:
                The maximum number of items each request retrieve.
                For search, this should not be more than 50.
                Default is 25.
            page_token:
                The token of the page of search result to retrieve.
                You can use this retrieve point result page directly.
                And you should know about the the result set for YouTube.
            return_json:
                The return data type. If you set True JSON data will be returned.
                False will return a pyyoutube.SearchListResponse instance.
            kwargs:
                If you want use this pass more args. You can use this.

        Returns:
            SearchListResponse or original data
        """
        return self.search(
            for_developer=True,
            search_type="video",
            parts=parts,
            q=q,
            count=count,
            limit=limit,
            page_token=page_token,
            return_json=return_json,
            **kwargs,
        )

    def search_by_mine(
        self,
        *,
        parts: Optional[Union[str, list, tuple, set]],
        q: Optional[str] = None,
        count: Optional[int] = 25,
        limit: Optional[int] = 25,
        page_token: Optional[str] = None,
        return_json: Optional[bool] = False,
        **kwargs,
    ) -> Union[SearchListResponse, dict]:
        """
        Parameter restricts the search to only retrieve videos owned by the authenticated user.

        Note:
            This methods can not use following parameters:
            video_definition, video_dimension, video_duration, video_license,
            video_embeddable, video_syndicated, video_type.
        Args:
            q:
                Your keywords can also use the Boolean NOT (-) and OR (|) operators to exclude videos or
                to find videos that are associated with one of several search terms. For example,
                to search for videos matching either "boating" or "sailing",
                set the q parameter value to boating|sailing. Similarly,
                to search for videos matching either "boating" or "sailing" but not "fishing",
                set the q parameter value to boating|sailing -fishing.
                Note that the pipe character must be URL-escaped when it is sent in your API request.
                The URL-escaped value for the pipe character is %7C.
            parts ((str,list,tuple,set) optional):
                The resource parts for you want to retrieve.
                If not provide, use default public parts.
                You can pass this with single part str, comma-separated parts str or a list,tuple,set of parts.
            count (int, optional):
                The count will retrieve videos data.
                Default is 25.
            limit (int, optional):
                The maximum number of items each request retrieve.
                For search, this should not be more than 50.
                Default is 25.
            page_token (str, optional):
                The token of the page of search result to retrieve.
                You can use this retrieve point result page directly.
                And you should know about the the result set for YouTube.
            return_json(bool, optional):
                The return data type. If you set True JSON data will be returned.
                False will return a pyyoutube.SearchListResponse instance.
            kwargs:
                If you want use this pass more args. You can use this.

        Returns:
            SearchListResponse or original data
        """
        return self.search(
            for_mine=True,
            search_type="video",
            parts=parts,
            q=q,
            count=count,
            limit=limit,
            page_token=page_token,
            return_json=return_json,
            **kwargs,
        )

    def search_by_related_video(
        self,
        *,
        related_to_video_id: str,
        parts: Optional[Union[str, list, tuple, set]] = None,
        region_code: Optional[str] = None,
        relevance_language: Optional[str] = None,
        safe_search: Optional[str] = None,
        count: Optional[int] = 25,
        limit: Optional[int] = 25,
        page_token: Optional[str] = None,
        return_json: Optional[bool] = False,
    ) -> Union[SearchListResponse, dict]:
        """
        Retrieve a list of videos related to that video.

        Args:
            related_to_video_id:
                 A YouTube video ID which result associated with.
            parts:
                The resource parts for you want to retrieve.
                If not provide, use default public parts.
                You can pass this with single part str, comma-separated parts str or a list,tuple,set of parts.
            region_code:
                Parameter instructs the API to return search results for videos
                that can be viewed in the specified country.
            relevance_language:
                Parameter instructs the API to return search results that are most relevant to the specified language.
            safe_search:
                Parameter indicates whether the search results should include restricted content
                as well as standard content.
                Acceptable values are:
                    - moderate – YouTube will filter some content from search results and, at the least,
                      will filter content that is restricted in your locale. Based on their content,
                      search results could be removed from search results or demoted in search results.
                      This is the default parameter value.
                    - none – YouTube will not filter the search result set.
                    - strict – YouTube will try to exclude all restricted content from the search result set.
                      Based on their content, search results could be removed from search results or
                      demoted in search results.
            count:
                The count will retrieve videos data.
                Default is 25.
            limit:
                The maximum number of items each request retrieve.
                For search, this should not be more than 50.
                Default is 25.
            page_token:
                The token of the page of search result to retrieve.
                You can use this retrieve point result page directly.
                And you should know about the the result set for YouTube.
            return_json:
                The return data type. If you set True JSON data will be returned.
                False will return a pyyoutube.SearchListResponse instance.
        Returns:
            If you want use this pass more args. You can use this.
        """

        return self.search(
            parts=parts,
            related_to_video_id=related_to_video_id,
            search_type="video",
            region_code=region_code,
            relevance_language=relevance_language,
            safe_search=safe_search,
            count=count,
            limit=limit,
            page_token=page_token,
            return_json=return_json,
        )

    def get_subscription_by_id(
        self,
        *,
        subscription_id: Union[str, list, tuple, set],
        parts: Optional[Union[str, list, tuple, set]] = None,
        return_json: Optional[bool] = False,
    ):
        """
        Retrieve subscriptions by given subscription id(s).

        Note:
            This need authorized access token. or you will get no data.

        Args:
            subscription_id ((str,list,tuple,set)):
                The id for subscription that you want to retrieve data.
                You can pass this with single id str, comma-separated id str, or a list,tuple,set of ids.
            parts ((str,list,tuple,set), optional):
                The resource parts for you want to retrieve.
                If not provide, use default public parts.
                You can pass this with single part str, comma-separated parts str or a list,tuple,set of parts.
            return_json(bool, optional):
                The return data type. If you set True JSON data will be returned.
                False will return a pyyoutube.SubscriptionListResponse instance.
        Returns:
            SubscriptionListResponse or original data.
        """

        args = {
            "id": enf_comma_separated(field="subscription_id", value=subscription_id),
            "part": enf_parts(resource="subscriptions", value=parts),
        }

        resp = self._request(resource="subscriptions", method="GET", args=args)
        data = self._parse_response(resp)

        if return_json:
            return data
        else:
            return SubscriptionListResponse.from_dict(data)

    def get_subscription_by_channel(
        self,
        *,
        channel_id: str,
        parts: Optional[Union[str, list, tuple, set]] = None,
        for_channel_id: Optional[Union[str, list, tuple, set]] = None,
        order: Optional[str] = "relevance",
        count: Optional[int] = 20,
        limit: Optional[int] = 20,
        page_token: Optional[str] = None,
        return_json: Optional[bool] = False,
    ):
        """
        Retrieve the specified channel's subscriptions.

        Note:
             The API returns a 403 (Forbidden) HTTP response code if the specified channel
             does not publicly expose its subscriptions and the request is not authorized
             by the channel's owner.

        Args:
            channel_id (str):
                The id for channel which you want to get subscriptions.
            parts ((str,list,tuple,set) optional):
                The resource parts for subscription you want to retrieve.
                If not provide, use default public parts.
                You can pass this with single part str, comma-separated parts str or a list,tuple,set of parts.
            for_channel_id ((str,list,tuple,set) optional):
                The parameter specifies a comma-separated list of channel IDs.
                and will then only contain subscriptions matching those channels.
                You can pass this with single part str, comma-separated parts str or a list,tuple,set of channel ids.
            order (str, optional):
                The parameter specifies the method that will be used to sort resources in the API response.
                Acceptable values are:
                    alphabetical – Sort alphabetically.
                    relevance – Sort by relevance.
                    unread – Sort by order of activity.
                Default is relevance
            count (int, optional):
                The count will retrieve subscriptions data.
                Default is 20.
                If provide this with None, will retrieve all subscriptions.
            limit (int, optional):
                The maximum number of items each request retrieve.
                For comment threads, this should not be more than 50.
                Default is 20.
            page_token(str, optional):
                The token of the page of subscriptions result to retrieve.
                You can use this retrieve point result page directly.
                And you should know about the the result set for YouTube.
            return_json(bool, optional):
                The return data type. If you set True JSON data will be returned.
                False will return a pyyoutube.SubscriptionListResponse instance.
        Returns:
            SubscriptionListResponse or original data.
        """

        if count is None:
            limit = 50  # for subscriptions the max limit for per request is 50
        else:
            limit = min(count, limit)

        args = {
            "channelId": channel_id,
            "part": enf_parts(resource="subscriptions", value=parts),
            "order": order,
            "maxResults": limit,
        }

        if for_channel_id is not None:
            args["forChannelId"] = enf_comma_separated(
                field="for_channel_id", value=for_channel_id
            )

        if page_token is not None:
            args["pageToken"] = page_token

        res_data = self.paged_by_page_token(
            resource="subscriptions", args=args, count=count
        )
        if return_json:
            return res_data
        else:
            return SubscriptionListResponse.from_dict(res_data)

    def get_subscription_by_me(
        self,
        *,
        mine: Optional[bool] = None,
        recent_subscriber: Optional[bool] = None,
        subscriber: Optional[bool] = None,
        parts: Optional[Union[str, list, tuple, set]] = None,
        for_channel_id: Optional[Union[str, list, tuple, set]] = None,
        order: Optional[str] = "relevance",
        count: Optional[int] = 20,
        limit: Optional[int] = 20,
        page_token: Optional[str] = None,
        return_json: Optional[bool] = False,
    ):
        """
        Retrieve your subscriptions.

        Note:
            This can only used in a properly authorized request.
            And for me test the parameter `recent_subscriber` and `subscriber` maybe not working.
            Use the `mine` first.

        Args:
            mine (bool, optional):
                Set this parameter's value to True to retrieve a feed of the authenticated user's subscriptions.
            recent_subscriber (bool, optional):
                Set this parameter's value to true to retrieve a feed of the subscribers of the authenticated user
                in reverse chronological order (newest first).
                And this can only get most recent 1000 subscribers.
            subscriber (bool, optional):
                Set this parameter's value to true to retrieve a feed of the subscribers of
                the authenticated user in no particular order.
            parts ((str,list,tuple,set) optional):
                The resource parts for subscription you want to retrieve.
                If not provide, use default public parts.
                You can pass this with single part str, comma-separated parts str or a list,tuple,set of parts.
            for_channel_id ((str,list,tuple,set) optional):
                The parameter specifies a comma-separated list of channel IDs.
                and will then only contain subscriptions matching those channels.
                You can pass this with single part str, comma-separated parts str or a list,tuple,set of channel ids.
            order (str, optional):
                The parameter specifies the method that will be used to sort resources in the API response.
                Acceptable values are:
                    alphabetical – Sort alphabetically.
                    relevance – Sort by relevance.
                    unread – Sort by order of activity.
                Default is relevance
            count (int, optional):
                The count will retrieve subscriptions data.
                Default is 20.
                If provide this with None, will retrieve all subscriptions.
            limit (int, optional):
                The maximum number of items each request retrieve.
                For subscriptions, this should not be more than 50.
                Default is 20.
            page_token(str, optional):
                The token of the page of subscriptions result to retrieve.
                You can use this retrieve point result page directly.
                And you should know about the the result set for YouTube.
            return_json(bool, optional):
                The return data type. If you set True JSON data will be returned.
                False will return a pyyoutube.SubscriptionListResponse instance.

        Returns:
            SubscriptionListResponse or original data.
        """

        if count is None:
            limit = 50  # for subscriptions the max limit for per request is 50
        else:
            limit = min(count, limit)

        args = {
            "part": enf_parts(resource="subscriptions", value=parts),
            "order": order,
            "maxResults": limit,
        }

        if mine is not None:
            args["mine"] = mine
        elif recent_subscriber is not None:
            args["myRecentSubscribers"] = recent_subscriber
        elif subscriber is not None:
            args["mySubscribers"] = subscriber
        else:
            raise PyYouTubeException(
                ErrorMessage(
                    status_code=ErrorCode.MISSING_PARAMS,
                    message=f"Must specify at least one of mine,recent_subscriber,subscriber.",
                )
            )

        if for_channel_id is not None:
            args["forChannelId"] = enf_comma_separated(
                field="for_channel_id", value=for_channel_id
            )

        if page_token is not None:
            args["pageToken"] = page_token

        res_data = self.paged_by_page_token(
            resource="subscriptions", args=args, count=count
        )
        if return_json:
            return res_data
        else:
            return SubscriptionListResponse.from_dict(res_data)

    def get_video_abuse_report_reason(
        self,
        *,
        parts: Optional[Union[str, list, tuple, set]] = None,
        hl: Optional[str] = "en_US",
        return_json: Optional[bool] = False,
    ) -> Union[VideoAbuseReportReasonListResponse, dict]:
        """
        Retrieve a list of reasons that can be used to report abusive videos.

        Notes:
            This requires your authorization.

        Args:
            parts:
                The resource parts for abuse reason you want to retrieve.
                If not provide, use default public parts.
                You can pass this with single part str, comma-separated parts str or a list,tuple,set of parts.
            hl:
                If provide this. Will return report reason's language localized info.
                This value need https://developers.google.com/youtube/v3/docs/i18nLanguages.
            return_json:
                The return data type. If you set True JSON data will be returned.
                False will return a pyyoutube.VideoAbuseReportReasonListResponse instance.
        Returns:
            VideoAbuseReportReasonListResponse or original data.
        """

        args = {
            "part": enf_parts(resource="videoAbuseReportReasons", value=parts),
            "hl": hl,
        }

        resp = self._request(resource="videoAbuseReportReasons", args=args)
        data = self._parse_response(resp)

        if return_json:
            return data
        else:
            return VideoAbuseReportReasonListResponse.from_dict(data)

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
        args = {
            "part": enf_parts(resource="videoCategories", value=parts),
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

        resp = self._request(resource="videoCategories", method="GET", args=args)
        data = self._parse_response(resp)

        if return_json:
            return data
        else:
            return VideoCategoryListResponse.from_dict(data)

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
        page_token: Optional[str] = None,
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
                If provide this with None, will retrieve all videos.
            limit (int, optional):
                The maximum number of items each request retrieve.
                For videos, this should not be more than 50.
                Default is 5.
            page_token(str, optional):
                The token of the page of videos result to retrieve.
                You can use this retrieve point result page directly.
                And you should know about the the result set for YouTube.
            return_json(bool, optional):
                The return data type. If you set True JSON data will be returned.
                False will return a pyyoutube.PlaylistListResponse instance.

        Returns:
            VideoListResponse or original data
        """

        if count is None:
            limit = 50  # for videos the max limit for per request is 50
        else:
            limit = min(count, limit)

        args = {
            "chart": chart,
            "part": enf_parts(resource="videos", value=parts),
            "hl": hl,
            "maxResults": limit,
            "videoCategoryId": category_id,
        }
        if max_height is not None:
            args["maxHeight"] = max_height
        if max_width is not None:
            args["maxWidth"] = max_width
        if region_code:
            args["regionCode"] = region_code

        if page_token is not None:
            args["pageToken"] = page_token

        res_data = self.paged_by_page_token(resource="videos", args=args, count=count)
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
        page_token: Optional[str] = None,
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
                If provide this with None, will retrieve all videos.
            limit (int, optional):
                The maximum number of items each request retrieve.
                For videos, this should not be more than 50.
                Default is 5.
            page_token(str, optional):
                The token of the page of videos result to retrieve.
                You can use this retrieve point result page directly.
                And you should know about the the result set for YouTube.
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

        if count is None:
            limit = 50  # for videos the max limit for per request is 50
        else:
            limit = min(count, limit)

        args = {
            "myRating": rating,
            "part": enf_parts(resource="videos", value=parts),
            "hl": hl,
            "maxResults": limit,
        }

        if max_height is not None:
            args["maxHeight"] = max_height
        if max_width is not None:
            args["maxWidth"] = max_width

        if page_token is not None:
            args["pageToken"] = page_token

        res_data = self.paged_by_page_token(resource="videos", args=args, count=count)
        if return_json:
            return res_data
        else:
            return VideoListResponse.from_dict(res_data)
