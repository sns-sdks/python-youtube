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
from pyyoutube.models import AccessToken


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
            access_token=None, timeout=None
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
                timeout=self._timeout
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
    def _parse_response(response):
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
        return data
