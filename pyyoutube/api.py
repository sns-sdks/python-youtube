"""
    Main Api implementation.
"""
try:
    from urllib.parse import urlencode, urlparse, parse_qsl
except ImportError:
    from urllib import urlecode
    from urlparse import urlparse, parse_qsl

import requests
from requests.models import Response

from pyyoutube.error import ErrorMessage, PyYouTubeException
from pyyoutube.models import AccessToken, UserProfile, Channel, Video


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

    def __init__(
            self, client_id, client_secret, api_key=None,
            access_token=None, timeout=None, proxies=None
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

    @staticmethod
    def _parse_response(response, api=False):
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
            items = data['items']
            if isinstance(items, dict) or len(items) == 0:
                raise PyYouTubeException(response)
            else:
                return items[0]
        return data

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
                'part': 'id,snippet,contentDetails,statistics'
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
        if return_json:
            return data
        else:
            return Channel.new_from_json_dict(data)

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
            'part': 'id,snippet,contentDetails,statistics'
        }

        resp = self._request(
            resource='videos',
            method='GET',
            args=args
        )

        data = self._parse_response(resp, api=True)

        if return_json:
            return data
        else:
            return
