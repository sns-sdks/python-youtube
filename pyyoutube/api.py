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
    Channel,
)
from pyyoutube.model import (
    Comment,
    CommentThread,
    GuideCategory,
    PlayList,
    PlaylistItem,
    Video,
    VideoCategory,
)
from pyyoutube.utils import constants
from pyyoutube.utils.params_checker import (
    comma_separated_validator,
    incompatible_validator,
    parts_validator,
)
from pyyoutube.utils.decorators import (
    comma_separated,
    incompatible,
    parts_validator as parts_checker,
)


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

    def _parse_response(
        self, response: Response, api: Optional[bool] = False
    ) -> Union[dict, list]:
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
        if api:
            return self._parse_data(data)
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
                ErrorMessage(status_code=ErrorCode.HTTP_ERROR, message=e.args)
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
                ErrorMessage(status_code=ErrorCode.HTTP_ERROR, message=e.args)
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

    @comma_separated(params=["channel_id"])
    @parts_checker(resource="channels")
    @incompatible(params=["channel_id", "channel_name", "mine"])
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

        args = {"hl": hl, "part": parts}
        if channel_name is not None:
            args["forUsername"] = channel_name
        elif channel_id is not None:
            args["id"] = channel_id
        elif mine is not None:
            args["mine"] = mine

        resp = self._request(resource="channels", method="GET", args=args)

        data = self._parse_response(resp, api=True)
        if return_json:
            return data
        else:
            return [Channel.from_dict(item) for item in data]

    @comma_separated(params=["playlist_id"])
    @parts_checker(resource="playlists")
    @incompatible(params=["channel_id", "playlist_id", "mine"])
    def get_playlist(
        self,
        *,
        channel_id: Optional[str] = None,
        playlist_id: Optional[Union[str, list, tuple, set]] = None,
        mine: Optional[bool] = None,
        parts: Optional[Union[str, list, tuple, set]] = None,
        summary: Optional[bool] = True,
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
            playlist_id (str optional)
                If provide this. will return those playlist's info.
                You can pass this with single id str,comma-separated id str,
                or list, tuple, set of id str.
            mine (bool, optional)
                If you have give the authorization. Will return your playlists.
                Must provide the access token.
            parts (str, optional)
                Comma-separated list of one or more playlist resource properties.
                You can also pass this with list, tuple, set of part str.
                If not provided. will use default public properties.
            summary (bool, optional)
                 If True will return channel playlist summary of metadata.
                 Notice this depend on your query.
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
            return tuple.
            (playlist data, playlist summary)
        """

        args = {"part": parts, "hl": hl, "maxResults": min(count, limit)}

        if channel_id is not None:
            args["channelId"] = channel_id
        elif playlist_id is not None:
            args["id"] = playlist_id
        elif mine is not None:
            args["mine"] = mine

        playlists = []
        playlists_summary = None
        next_page_token = None
        while True:
            prev_page_token, next_page_token, data = self.paged_by_page_token(
                resource="playlists", args=args, page_token=next_page_token,
            )
            items = self._parse_data(data)
            if return_json:
                playlists += items
            else:
                playlists += [PlayList.new_from_json_dict(item) for item in items]
            if summary:
                playlists_summary = data.get("pageInfo", {})
            if next_page_token is None:
                break
            if len(playlists) >= count:
                break
        return playlists[:count], playlists_summary

    def get_playlist_item(
        self,
        playlist_id=None,
        playlist_item_id=None,
        video_id=None,
        parts=None,
        summary=True,
        count=5,
        limit=5,
        return_json=False,
    ):
        """
        Retrieve channel's playlist Items info.

        Args:
            playlist_id (str, optional)
                If provide channel id, this will return pointed playlist's item info.
            playlist_item_id (str optional)
                If provide this. will return those playlistItem's info.
            video_id (str, optional)
                If provide this, will return playlist items which contain the specify video.
            parts (str, optional)
                Comma-separated list of one or more playlist items resource properties.
                If not provided. will use default public properties.
            summary (bool, optional)
                 If True will return playlist item summary of metadata.
                 Notice this depend on your query.
            count (int, optional)
                The count will retrieve playlist items data.
                Default is 5.
            limit (int, optional)
                The maximum number of items each request retrieve.
                For playlistItem, this should not be more than 50.
                Default is 5
            return_json(bool, optional)
                The return data type. If you set True JSON data will be returned.
                False will return pyyoutube.PlayListItem
        Returns:
            return tuple.
            (playlistItem data, playlistItem summary)
        """
        comma_separated_validator(playlist_item_id=playlist_item_id, parts=parts)
        incompatible_validator(
            playlist_id=playlist_id, playlist_item_id=playlist_item_id
        )

        if parts is None:
            parts = constants.PLAYLIST_ITEM_RESOURCE_PROPERTIES
            parts = ",".join(parts)
        else:
            parts_validator("playlistItems", parts=parts)

        args = {
            "part": parts,
            "maxResults": limit,
        }

        if playlist_id is not None:
            args["playlistId"] = playlist_id
        elif playlist_item_id is not None:
            args["id"] = playlist_item_id

        if video_id is not None:
            args["videoId"] = video_id

        playlist_items = []
        playlist_items_summary = None
        next_page_token = None
        while True:
            prev_page_token, next_page_token, data = self.paged_by_page_token(
                resource="playlistItems", args=args, page_token=next_page_token,
            )
            items = self._parse_data(data)
            if return_json:
                playlist_items += items
            else:
                playlist_items += [
                    PlaylistItem.new_from_json_dict(item) for item in items
                ]
            if summary:
                playlist_items_summary = data.get("pageInfo", {})
            if next_page_token is None:
                break
            if len(playlist_items) >= count:
                break
        return playlist_items[:count], playlist_items_summary

    def get_video_by_id(self, video_id=None, hl="en_US", parts=None, return_json=False):
        """
        Retrieve data from YouTube Data Api for video which id or id list you point .

        Args:
            video_id (str)
                The id or comma-separated id list of video which you want to get data.
            hl (str, optional)
                If provide this. Will return video snippet's language localized info.
                This value need https://developers.google.com/youtube/v3/docs/i18nLanguages.
            parts (str, optional)
                Comma-separated list of one or more videos resource properties.
                If not provided. will use default public properties.
            return_json(bool, optional)
                The return data type. If you set True JSON data will be returned.
                False will return pyyoutube.Video
        Returns:
            The data for you given video.
        """
        comma_separated_validator(video_id=video_id, parts=parts)
        incompatible_validator(video_id=video_id)

        if parts is None:
            parts = constants.VIDEO_RESOURCE_PROPERTIES
            parts = ",".join(parts)
        else:
            parts_validator("videos", parts=parts)

        args = {
            "id": video_id,
            "hl": hl,
            "part": parts,
        }

        resp = self._request(resource="videos", method="GET", args=args)

        data = self._parse_response(resp, api=True)
        if return_json:
            return data
        else:
            return [Video.new_from_json_dict(item) for item in data]

    def get_video_by_filter(
        self,
        chart=None,
        my_rating=None,
        region_code=None,
        category_id=None,
        summary=True,
        count=5,
        limit=5,
        hl="en_US",
        parts=None,
        return_json=False,
    ):
        """
        Retrieve data from YouTube Data Api for video which you point.

        Args:
            chart (str, optional)
                Now only mostPopular parameter valid.
                Will return most popular videos for point region or category.
                If use this must provide either region code or category id.
            my_rating(str, optional)
                Now dislike and like parameter can be pointed.
                - dislike will return set disliked by you.
                - like will return set liked by you.
                Must need you give authorization.
            region_code (str, optional)
                Provide region code for filter for the chart parameter.
            category_id (str, optional)
                Provide video category id for filter for the chart parameter.
            summary (bool, optional)
                 If True will return results videos summary of metadata.
                 Notice this depend on your query.
            count (int, optional)
                The count will retrieve videos data.
                Default is 5.
            limit (int, optional)
                The maximum number of items each request retrieve.
                For videos, this should not be more than 50.
                Default is 5
            hl (str, optional)
                If provide this. Will return video snippet's language localized info.
                This value need https://developers.google.com/youtube/v3/docs/i18nLanguages.
            parts (str, optional)
                Comma-separated list of one or more playlist items resource properties.
                If not provided. will use default public properties.
            return_json(bool, optional)
                The return data type. If you set True JSON data will be returned.
                False will return pyyoutube.Video
        Returns:
            The data for videos by your filter.
        """

        comma_separated_validator(parts=parts)
        incompatible_validator(chart=chart, my_rating=my_rating)

        if parts is None:
            parts = constants.VIDEO_RESOURCE_PROPERTIES
            parts = ",".join(parts)
        else:
            parts_validator("videos", parts=parts)

        args = {"part": parts, "hl": hl, "maxResults": limit}

        if chart is not None:
            args["chart"] = chart
            if region_code is not None:
                args["regionCode"] = region_code
            elif category_id is not None:
                args["videoCategoryId"] = category_id
        elif my_rating is not None:
            args["myRating"] = my_rating

        videos = []
        videos_summary = None
        next_page_token = None
        while True:
            prev_page_token, next_page_token, data = self.paged_by_page_token(
                resource="videos", args=args, page_token=next_page_token,
            )
            items = self._parse_data(data)
            if return_json:
                videos += items
            else:
                videos += [Video.new_from_json_dict(item) for item in items]
            if summary:
                videos_summary = data.get("pageInfo", {})
            if next_page_token is None:
                break
            if len(videos) >= count:
                break
        return videos[:count], videos_summary

    def get_comment_threads(
        self,
        all_to_channel_id=None,
        channel_id=None,
        video_id=None,
        parts=None,
        order="time",
        search_term=None,
        limit=20,
        count=20,
        return_json=False,
    ):
        """
        Retrieve the comment thread info by single id.

        Refer: https://developers.google.com/youtube/v3/docs/commentThreads/list

        Args:
            all_to_channel_id (str, optional)
                If you provide channel id by this parameter.
                Will return all comment threads associated with the specified channel.
                The response can include comments about the channel or about the channel's videos.
            channel_id (str, optional)
                If you provide channel id by this parameter.
                Will return comment threads containing comments about the specified channel.
                But not include comments about the channel's videos.
            video_id (str, optional)
                If you provide video id by this parameter.
                Will return comment threads containing comments about the specified video.
            parts (str, optional)
                Comma-separated list of one or more commentThreads resource properties.
                If not provided. will use default public properties.
            order (str, optional)
                Provide the response order type. Valid value are: time, relevance.
                Default is time. order by the commented time.
            search_term (str, optional)
                If you provide this. Only return the comments that contain the search terms.
            limit (int, optional)
                Each request retrieve comment threads from data api.
                For comment threads, this should not be more than 100.
                Default is 20.
            count (int, optional)
                The count will retrieve comment threads data.
                Default is 20.
            return_json(bool, optional)
                The return data type. If you set True JSON data will be returned.
                False will return pyyoutube.CommentThread.
        Returns:
            The list data for you given comment thread.
        """

        comma_separated_validator(parts=parts)
        incompatible_validator(
            all_to_channel_id=all_to_channel_id,
            channel_id=channel_id,
            video_id=video_id,
        )
        if parts is None:
            parts = constants.COMMENT_THREAD_RESOURCE_PROPERTIES
            parts = ",".join(parts)
        else:
            parts_validator("commentThreads", parts=parts)

        args = {"part": parts, "maxResults": limit}
        if all_to_channel_id is not None:
            args["allThreadsRelatedToChannelId"] = all_to_channel_id
        elif channel_id is not None:
            args["channelId"] = channel_id
        elif video_id is not None:
            args["videoId"] = video_id

        if order not in ["time", "relevance"]:
            raise PyYouTubeException(
                ErrorMessage(
                    status_code=ErrorCode.INVALID_PARAMS,
                    message="Order type must be time or relevance.",
                )
            )

        if search_term is not None:
            args["searchTerms"] = search_term

        comment_threads = []
        next_page_token = None
        while True:
            _, next_page_token, data = self.paged_by_page_token(
                resource="commentThreads", args=args, page_token=next_page_token,
            )
            items = self._parse_data(data)
            if return_json:
                comment_threads += items
            else:
                comment_threads += [
                    CommentThread.new_from_json_dict(item) for item in items
                ]
            if next_page_token is None:
                break
            if len(comment_threads) >= count:
                break
        return comment_threads[:count]

    def get_comment_thread_info(
        self, comment_thread_id=None, parts=None, return_json=False
    ):
        """
        Retrieve the comment thread info by single id.

        Refer: https://developers.google.com/youtube/v3/docs/commentThreads/list

        Args:
            comment_thread_id (str)
                The id parameter specifies a comma-separated list of comment thread IDs
                for the resources that should be retrieved.
            parts (str, optional)
                Comma-separated list of one or more commentThreads resource properties.
                If not provided. will use default public properties.
            return_json(bool, optional)
                The return data type. If you set True JSON data will be returned.
                False will return pyyoutube.CommentThread.
        Returns:
            The list data for you given comment thread.
        """

        comma_separated_validator(comment_thread_id=comment_thread_id, parts=parts)
        incompatible_validator(comment_thread_id=comment_thread_id)
        if parts is None:
            parts = constants.COMMENT_THREAD_RESOURCE_PROPERTIES
            parts = ",".join(parts)
        else:
            parts_validator("commentThreads", parts=parts)

        args = {"id": comment_thread_id, "part": parts}

        resp = self._request(resource="commentThreads", args=args)

        data = self._parse_response(resp, api=True)
        if return_json:
            return data
        else:
            return [CommentThread.new_from_json_dict(item) for item in data]

    def get_comments_by_parent(
        self, parent_id=None, parts=None, limit=20, count=20, return_json=False
    ):
        """
        Retrieve data from YouTube Data Api for top level comment which you point.

        Refer: https://developers.google.com/youtube/v3/docs/comments/list

        Args:
            parent_id (str, optional)
                Provide the ID of the comment for which replies should be retrieved.
                Now YouTube currently supports replies only for top-level comments
            parts (str, optional)
                Comma-separated list of one or more comments resource properties.
                If not provided. will use default public properties.
            limit (int, optional)
                Each request retrieve comments from data api.
                For comments, this should not be more than 100.
                Default is 20.
            count (int, optional)
                The count will retrieve comments data.
                Default is 20.
            return_json(bool, optional)
                The return data type. If you set True JSON data will be returned.
                False will return pyyoutube.Comment.
        Returns:
            The list data for you given comment.
        """

        comma_separated_validator(parts=parts)
        incompatible_validator(parent_id=parent_id)
        if parts is None:
            parts = constants.COMMENT_RESOURCE_PROPERTIES
            parts = ",".join(parts)
        else:
            parts_validator("comments", parts=parts)

        args = {"part": parts, "maxResults": limit, "parentId": parent_id}

        comments = []
        next_page_token = None
        while True:
            _, next_page_token, data = self.paged_by_page_token(
                resource="comments", args=args, page_token=next_page_token,
            )
            items = self._parse_data(data)
            if return_json:
                comments += items
            else:
                comments += [Comment.new_from_json_dict(item) for item in items]
            if len(comments) >= count:
                break
            if next_page_token is None:
                break
        return comments[:count]

    def get_comment_info(self, comment_id=None, parts=None, return_json=False):
        """
        Retrieve comment data by comment id.

        Args:
            comment_id (str, optional)
                Provide a comma-separated list of comment IDs or just a comment id
                for the resources that are being retrieved
            parts (str, optional)
                Comma-separated list of one or more comments resource properties.
                If not provided. will use default public properties.
            return_json(bool, optional)
                The return data type. If you set True JSON data will be returned.
                False will return pyyoutube.Comment.
        Returns:
            The list data for you given comment id.
        """
        comma_separated_validator(comment_id=comment_id, parts=parts)
        incompatible_validator(comment_id=comment_id)
        if parts is None:
            parts = constants.COMMENT_RESOURCE_PROPERTIES
            parts = ",".join(parts)
        else:
            parts_validator("comments", parts=parts)

        args = {"part": parts, "id": comment_id}

        resp = self._request(resource="comments", args=args)
        data = self._parse_response(resp, api=True)
        if return_json:
            return data
        else:
            return [Comment.new_from_json_dict(item) for item in data]

    def get_video_categories(
        self,
        category_id=None,
        region_code=None,
        parts=None,
        hl="en_US",
        return_json=False,
    ):
        """
        Retrieve a list of categories that can be associated with YouTube videos.

        Refer: https://developers.google.com/youtube/v3/docs/videoCategories

        Args:
            category_id (str, optional)
                Provide a comma-separated list of video category IDs or just a video category id
                for the resources that are being retrieved.
            region_code (str, optional)
                Provide country code for the list of video categories available.
                The country code is an ISO 3166-1 alpha-2 country code.
            parts (str, optional)
                Comma-separated list of one or more videoCategories resource properties.
                If not provided. will use default public properties.
            hl (str, optional)
                Specifies the language that should be used for text values.
                Default is en_US.
            return_json (bool, optional)
                The return data type. If you set True JSON data will be returned.
                False will return pyyoutube.VideoCategory.
        Returns:
            The list of categories.
        """
        comma_separated_validator(category_id=category_id, parts=parts)
        incompatible_validator(category_id=category_id, region_code=region_code)
        if parts is None:
            parts = constants.VIDEO_CATEGORY_RESOURCE_PROPERTIES
            parts = ",".join(parts)
        else:
            parts_validator("videoCategories", parts=parts)

        args = {
            "part": parts,
            "hl": hl,
        }

        if category_id is not None:
            args["id"] = category_id
        elif region_code is not None:
            args["regionCode"] = region_code

        resp = self._request(resource="videoCategories", args=args)

        data = self._parse_response(resp, api=True)
        if return_json:
            return data
        else:
            return [VideoCategory.new_from_json_dict(item) for item in data]

    def get_guide_categories(
        self,
        category_id=None,
        region_code=None,
        parts=None,
        hl="en_US",
        return_json=False,
    ):
        """
        Retrieve a list of categories that can be associated with YouTube channels.

        Refer: https://developers.google.com/youtube/v3/docs/guideCategories

        Args:
            category_id (str, optional)
                Provide a comma-separated list of guide category IDs or just a guide category id
                for the resources that are being retrieved.
            region_code (str, optional)
                Provide country code for the list of guide categories available.
                The country code is an ISO 3166-1 alpha-2 country code.
            parts (str, optional)
                Comma-separated list of one or more guideCategories resource properties.
                If not provided. will use default public properties.
            hl (str, optional)
                Specifies the language that should be used for text values.
                Default is en_US.
            return_json (bool, optional)
                The return data type. If you set True JSON data will be returned.
                False will return pyyoutube.GuideCategory.

        Returns:
            The list of categories.
        """

        comma_separated_validator(category_id=category_id, parts=parts)
        incompatible_validator(category_id=category_id, region_code=region_code)
        if parts is None:
            parts = constants.GUIDE_CATEGORY_RESOURCE_PROPERTIES
            parts = ",".join(parts)
        else:
            parts_validator("guideCategories", parts=parts)

        args = {
            "part": parts,
            "hl": hl,
        }

        if category_id is not None:
            args["id"] = category_id
        elif region_code is not None:
            args["regionCode"] = region_code

        resp = self._request(resource="guideCategories", args=args)

        data = self._parse_response(resp, api=True)
        if return_json:
            return data
        else:
            return [GuideCategory.new_from_json_dict(item) for item in data]
