"""
    Main Api implementation.
"""

import datetime
from urllib.parse import urlencode, urlparse, parse_qsl

import pytz
import requests
from requests.models import Response  # noqa

from pyyoutube.error import ErrorMessage, PyYouTubeException
from pyyoutube.models import (
    AccessToken, UserProfile, Channel, Video,
    PlayList, PlaylistItem
)
from pyyoutube.utils.quota_cost import LIST_DATA


class Api(object):
    BASE_URL = 'https://www.googleapis.com/youtube/v3/'
    AUTHORIZATION_URL = 'https://accounts.google.com/o/oauth2/v2/auth'
    EXCHANGE_ACCESS_TOKEN_URL = 'https://www.googleapis.com/oauth2/v4/token'

    DEFAULT_REDIRECT_URI = 'http://127.0.0.1'

    DEFAULT_SCOPE = [
        'https://www.googleapis.com/auth/youtube',
        'https://www.googleapis.com/auth/userinfo.profile'
    ]

    DEFAULT_STATE = 'PyYouTube'
    DEFAULT_TIMEOUT = 10
    DEFAULT_QUOTA = 10000  # this quota reset at 00:00:00(GMT-7) every day.

    def __init__(
            self, client_id=None, client_secret=None, api_key=None,
            access_token=None, timeout=None, proxies=None, quota=None,
    ):
        """
        This Api provide two method to work. Use api key or use access token.

        Args:
            client_id(str, optional)
                Your google app's ID.
            client_secret (str, optional)
                Your google app's secret.
            api_key(str, optional)
                The api key which you create from google api console.
            access_token(str, optional)
                If you not provide api key, you can do authorization to get an access token.
            timeout(int, optional)
                The request timeout.
            proxies(dict, optional)
                If you want use proxy, need point this param.
                param style like requests lib style.
            quota(int, optional)
                if your key has more quota. you can point this. Default is 10000

        Returns:
            YouTube Api instance.
        """
        self._client_id = client_id
        self._client_secret = client_secret
        self._api_key = api_key
        self._access_token = access_token
        self._timeout = timeout
        self.session = requests.Session()
        self.scope = None
        self.proxies = proxies

        self.quota = quota
        if self.quota is None:
            self.quota = self.DEFAULT_QUOTA
        self.used_quota = 0

        if not ((self._client_id and self._client_secret) or self._api_key):
            raise PyYouTubeException(ErrorMessage(
                status_code=10001,
                message='Must specify either client key info or api key.'
            ))

        if self._timeout is None:
            self._timeout = self.DEFAULT_TIMEOUT

    def get_authorization_url(self, redirect_uri=None, scope=None, **kwargs):
        """
        Build authorization url to do authorize.

        Args:
            redirect_uri(str, optional)
                The uri you have set on your google app authorized uri.
                if you not provide, will use default uri: 'http://127.0.0.1'
                Must this uri in you app's authorized uri list.
            scope (list, optional)
                The scope you want give permission.
                If you not provide, will use default scope.
            kwargs(dict, optional)
                Some other params you want provide.
        Returns:
            The uri you can open on browser to do authorize.
        """
        if redirect_uri is None:
            redirect_uri = self.DEFAULT_REDIRECT_URI

        self.scope = scope
        if self.scope is None:
            self.scope = self.DEFAULT_SCOPE
        try:
            scope = ' '.join(self.scope)
        except TypeError:
            raise PyYouTubeException(ErrorMessage(
                status_code=10001,
                message='scope need a list type.'
            ))

        authorization_kwargs = {
            'client_id': self._client_id,
            'redirect_uri': redirect_uri,
            'scope': scope,
            'access_type': 'offline',
            'response_type': 'code',
            'state': self.DEFAULT_STATE,
        }
        if kwargs:
            authorization_kwargs.update(kwargs)

        return self.AUTHORIZATION_URL + '?' + urlencode(authorization_kwargs)

    def exchange_code_to_access_token(self, authorization_response, redirect_uri=None, return_json=False):
        """
        Use the google auth response to get access token

        Args:
            authorization_response (str)
                The response url for you give auth permission.
            redirect_uri (str, optional)
                The redirect url you have point when do authorization step.
                If you not provide will use default uri: http://127.0.0.1
            return_json (bool, optional):
                If True JSON data will be returned, instead of pyyoutube.AccessToken
        Return:
            Retrieved access token's info,  pyyoutube.AccessToken instance.
        """
        query = urlparse(authorization_response).query
        params = dict(parse_qsl(query))

        if 'code' not in params:
            raise PyYouTubeException(ErrorMessage(
                status_code=10002,
                message="Missing code parameter in authorization response."
            ))

        if params.get('state', None) != self.DEFAULT_STATE:
            raise PyYouTubeException(ErrorMessage(
                status_code=10002,
                message="Missing state parameter in authorization response."
            ))
        if redirect_uri is None:
            redirect_uri = self.DEFAULT_REDIRECT_URI

        kwargs = {
            'code': params['code'],
            'client_id': self._client_id,
            'client_secret': self._client_secret,
            'redirect_uri': redirect_uri,
            'grant_type': 'authorization_code'
        }

        return self._fetch_token(kwargs, return_json)

    def refresh_token(self, refresh_token=None, return_json=False):
        """
        Refresh token by api return refresh token.
        Args:
            refresh_token (str)
                The refresh token which the api returns.
                If you not provide. will use saved token when do exchange token step retrieve.
            return_json (bool, optional):
                If True JSON data will be returned, instead of pyyoutube.AccessToken
        Return:
            Retrieved new access token's info,  pyyoutube.AccessToken instance.
        """
        if refresh_token is None:
            refresh_token = self._refresh_token

        if refresh_token is None:
            raise PyYouTubeException(ErrorMessage(
                status_code=10003,
                message='You must provide a refresh token to get a new access token'
            ))
        kwargs = {
            'refresh_token': refresh_token,
            'client_id': self._client_id,
            'client_secret': self._client_secret,
            'grant_type': 'refresh_token'
        }
        return self._fetch_token(kwargs, return_json)

    def _fetch_token(self, params, return_json=False):
        """
        Use the google auth response to get access token

        Args:
            params (dict)
                The params to get access token.
            return_json (bool, optional):
                If True JSON data will be returned, instead of pyyoutube.AccessToken
        Return:
            Retrieved access token's info,  pyyoutube.AccessToken instance.
        """
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        try:
            response = self.session.post(
                self.EXCHANGE_ACCESS_TOKEN_URL,
                data=params,
                headers=headers,
                timeout=self._timeout,
                proxies=self.proxies
            )
        except requests.HTTPError as e:
            raise PyYouTubeException(ErrorMessage(
                status_code=10000,
                message=e.read()
            ))
        data = self._parse_response(response)

        access_token = data['access_token']
        self._access_token = access_token
        # once get the refresh token. This token can be use long time.
        # refer: https://developers.google.com/identity/protocols/OAuth2
        refresh_token = data.get('refresh_token')
        if refresh_token is not None:
            self._refresh_token = refresh_token

        if return_json:
            return data
        else:
            return AccessToken.new_from_json_dict(data)

    def _parse_response(self, response, api=False):
        """
        Parse response data and check whether errors exists.
        Args:
            response (Response)
                The response which the request return.
        Return:
             response's data
        """
        data = response.json()
        if 'error' in data:
            raise PyYouTubeException(response)
        if api:
            return self._parse_data(data)
        return data

    @staticmethod
    def _parse_data(data):
        """
        Parse resp data
        Args:
            data (dict)
                The response data by response.json()
        Return:
             response's items
        """
        items = data['items']
        if isinstance(items, dict) or len(items) == 0:
            raise PyYouTubeException(ErrorMessage(
                status_code=10002,
                message='Response data not have items.'
            ))
        else:
            return items

    def _request(self, resource, method=None, args=None, post_args=None, enforce_auth=True):
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
            method = 'GET'

        if args is None:
            args = dict()

        if post_args is not None:
            method = 'POST'

        key = None
        access_token = None
        if self._access_token is not None:
            key = 'access_token'
            access_token = self._access_token
        if self._api_key is not None:
            key = 'key'
            access_token = self._api_key
        if access_token is None and enforce_auth:
            raise PyYouTubeException(ErrorMessage(
                status_code=10004,
                message='You must provide your credentials.'
            ))

        if enforce_auth:
            if method == 'POST' and key not in post_args:
                post_args[key] = access_token
            elif method == 'GET' and key not in args:
                args[key] = access_token

        try:
            response = self.session.request(
                method=method,
                url=self.BASE_URL + resource,
                timeout=self._timeout,
                params=args,
                data=post_args,
                proxies=self.proxies
            )
        except requests.HTTPError as e:
            raise PyYouTubeException(ErrorMessage(
                status_code=10000,
                message=e.read()
            ))
        else:
            return response

    def get_quota(self):
        pst = pytz.timezone('US/Pacific')
        now = datetime.datetime.now(pst)
        reset_at = (now + datetime.timedelta(1)).replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        reset_in = int((reset_at - now).total_seconds())
        return f"Quota(Total={self.quota}, Used={self.used_quota}, ResetIn={reset_in})"

    def calc_quota(self, resource, method='list', parts='', count=1):
        """
        :param resource: resources like videos, channels
        :param method:
        :param parts:
        :param count:
        :return:
        """
        if method == 'list':
            quota_data = LIST_DATA
        else:
            return 0
        cost = 1
        if parts:
            parts = parts.split(',')
        for part in parts:
            if part not in ['id']:
                need_cost = quota_data.get(f'{resource}.{part}', 0)
                cost += need_cost
        cost = cost * count
        self.used_quota += cost

    def get_profile(self, return_json=False):
        """

        """
        if self._access_token is None:
            raise PyYouTubeException(ErrorMessage(
                status_code=10005,
                message='Get profile Must need access token.'
            ))
        try:
            response = self.session.get(
                'https://www.googleapis.com/oauth2/v1/userinfo',
                params={'access_token': self._access_token},
                timeout=self._timeout,
                proxies=self.proxies
            )
        except requests.HTTPError as e:
            raise PyYouTubeException(ErrorMessage(
                status_code=10000,
                message=e.read()
            ))
        data = self._parse_response(response)
        if return_json:
            return data
        else:
            return UserProfile.new_from_json_dict(data)

    def get_channel_info(self, channel_id=None, channel_name=None, return_json=False):
        """
        Retrieve data from YouTube Data API for channel which you given.

        Args:
            channel_id (str, optional)
                The id for youtube channel. Id always likes: UCLA_DiR1FfKNvjuUpBHmylQ
            channel_name (str, optional)
                The name for youtube channel.
                If id and name all given, will use id first.
            return_json(bool, optional)
                The return data type. If you set True JSON data will be returned.
                False will return pyyoutube.Channel
        Returns:
            The data for you given channel.
        """
        if channel_name is not None:
            args = {
                'forUsername': channel_name,
                'part': 'id,snippet,contentDetails,statistics'
            }
        elif channel_id is not None:
            args = {
                'id': channel_id,
                'part': 'id,snippet,contentDetails,statistics,status'
            }
        else:
            raise PyYouTubeException(ErrorMessage(
                status_code=10005,
                message='Specify at least one of channel id or username'
            ))

        resp = self._request(
            resource='channels',
            method='GET',
            args=args
        )

        data = self._parse_response(resp, api=True)
        self.calc_quota(
            resource='channels',
            parts=args['part']
        )
        if return_json:
            return data
        else:
            return Channel.new_from_json_dict(data[0])

    def get_playlist(self,
                     channel_id=None,
                     playlist_id=None,
                     summary=True,
                     count=5,
                     limit=5,
                     return_json=False):
        """
        Retrieve channel playlists info.
        Provide two methods: by channel ID, or by playlist id (ids)

        Args:
            channel_id (str, optional)
                If provide channel id, this will return pointed channel's playlist info.
            playlist_id (str,list optional)
                If provide this. will return those playlist's info.
            summary (bool, optional)
                 If True will return channel playlist summary of metadata.
                 Notice this depend on your query.
            count (int, optional)
                The count will retrieve playlist data.
                Default is 5.
            limit (int, optional)
                Each request retrieve playlists from data api.
                For playlist, this should not be more than 50.
                Default is 5
            return_json(bool, optional)
                The return data type. If you set True JSON data will be returned.
                False will return pyyoutube.PlayList
        Returns:
            return tuple.
            (playlist data, playlist summary)
        """
        part = 'id,snippet,contentDetails,status,localizations'
        args = {
            'part': part,
            'maxResults': limit
        }
        if channel_id is not None:
            args['channelId'] = channel_id
        elif playlist_id is not None:
            if isinstance(playlist_id, str):
                p_id = playlist_id
            elif isinstance(playlist_id, (list, tuple)):
                p_id = ','.join(playlist_id)
            else:
                raise PyYouTubeException(ErrorMessage(
                    status_code=10007,
                    message='Playlist must be single id or id list.'
                ))
            args['id'] = p_id
        else:
            raise PyYouTubeException(ErrorMessage(
                status_code=10005,
                message='Specify at least one of channel id or playlist id(id list)'
            ))

        playlists = []
        playlists_summary = None
        next_page_token = None
        while True:
            prev_page_token, next_page_token, data = self.paged_by_page_token(
                resource='playlists',
                args=args,
                page_token=next_page_token,
            )
            items = self._parse_data(data)
            if return_json:
                playlists += items
            else:
                playlists += [PlayList.new_from_json_dict(item) for item in items]
            if summary:
                playlists_summary = data.get('pageInfo', {})
            if next_page_token is None:
                break
            if len(playlists) >= count:
                break
        return playlists[:count], playlists_summary

    def get_playlist_item(self,
                          playlist_id=None,
                          playlist_item_id=None,
                          summary=True,
                          count=5,
                          limit=5,
                          return_json=False):
        """
        Retrieve channel playlistItems info.
        Provide two methods: by playlist ID, or by playlistItem id (ids)

        Args:
            playlist_id (str, optional)
                If provide channel id, this will return pointed playlist's item info.
            playlist_item_id (str,list optional)
                If provide this. will return those playlistItem's info.
            summary (bool, optional)
                 If True will return playlist item summary of metadata.
                 Notice this depend on your query.
            count (int, optional)
                The count will retrieve playlist items data.
                Default is 5.
            limit (int, optional)
                Each request retrieve playlistItems from data api.
                For playlistItem, this should not be more than 50.
                Default is 5
            return_json(bool, optional)
                The return data type. If you set True JSON data will be returned.
                False will return pyyoutube.PlayListItem
        Returns:
            return tuple.
            (playlistItem data, playlistItem summary)
        """
        part = 'id,snippet,contentDetails,status'
        args = {
            'part': part,
            'maxResults': limit
        }
        if playlist_id is not None:
            args['playlistId'] = playlist_id
        elif playlist_item_id is not None:
            if isinstance(playlist_item_id, str):
                p_id = playlist_item_id
            elif isinstance(playlist_item_id, (list, tuple)):
                p_id = ','.join(playlist_item_id)
            else:
                raise PyYouTubeException(ErrorMessage(
                    status_code=10007,
                    message='PlaylistItem must be single id or id list.'
                ))
            args['id'] = p_id
        else:
            raise PyYouTubeException(ErrorMessage(
                status_code=10005,
                message='Specify at least one of channel id or playlist id(id list)'
            ))

        playlist_items = []
        playlist_items_summary = None
        next_page_token = None
        while True:
            prev_page_token, next_page_token, data = self.paged_by_page_token(
                resource='playlistItems',
                args=args,
                page_token=next_page_token,
            )
            items = self._parse_data(data)
            if return_json:
                playlist_items += items
            else:
                playlist_items += [PlaylistItem.new_from_json_dict(item) for item in items]
            if summary:
                playlist_items_summary = data.get('pageInfo', {})
            if next_page_token is None:
                break
            if len(playlist_items) >= count:
                break
        return playlist_items[:count], playlist_items_summary

    def get_video_info(self, video_id=None, return_json=False):
        """
        Retrieve data from YouTube Data Api for video which you point.

        Args:
            video_id (str)
                The video's ID which you want to get data.
            return_json(bool, optional)
                The return data type. If you set True JSON data will be returned.
                False will return pyyoutube.Video
        Returns:
            The data for you given video.
        """

        if video_id is None:
            raise PyYouTubeException(ErrorMessage(
                status_code=10005,
                message='Specify the id for the video.'
            ))

        args = {
            'id': video_id,
            'part': 'id,snippet,contentDetails,statistics,status'
        }

        resp = self._request(
            resource='videos',
            method='GET',
            args=args
        )

        data = self._parse_response(resp, api=True)
        self.calc_quota(
            resource='videos',
            parts=args['part']
        )
        if return_json:
            return data
        else:
            return Video.new_from_json_dict(data[0])

    def get_videos_info(self, video_ids=None, return_json=False):
        """
        Retrieve data from YouTube Data Api for video which you point.

        Args:
            video_ids (list)
                The video's ID list you want to get data.
            return_json(bool, optional)
                The return data type. If you set True JSON data will be returned.
                False will return pyyoutube.Video
        Returns:
            The data for you given video.
        """

        if video_ids is None or not isinstance(video_ids, (list, tuple)):
            raise PyYouTubeException(ErrorMessage(
                status_code=10005,
                message='Specify the id for the video.'
            ))

        args = {
            'id': ','.join(video_ids),
            'part': 'id,snippet,contentDetails,statistics,status'
        }

        resp = self._request(
            resource='videos',
            method='GET',
            args=args
        )

        data = self._parse_response(resp, api=True)
        self.calc_quota(
            resource='videos',
            parts=args['part'],
            count=len(video_ids)
        )
        if return_json:
            return data
        else:
            return [Video.new_from_json_dict(item) for item in data]

    def paged_by_page_token(self,
                            resource,
                            args,
                            page_token=None):
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
            args['pageToken'] = page_token

        resp = self._request(
            resource=resource,
            method='GET',
            args=args
        )
        data = self._parse_response(resp)  # origin response
        # set page token
        next_page_token = data.get('nextPageToken')
        prev_page_token = data.get('prevPageToken')
        return prev_page_token, next_page_token, data
