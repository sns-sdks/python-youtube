"""
    New Client for YouTube API
"""

import inspect
import json
from typing import List, Optional, Tuple, Union

import requests
from requests import Response
from requests.sessions import merge_setting
from requests.structures import CaseInsensitiveDict
from requests_oauthlib.oauth2_session import OAuth2Session

import pyyoutube.resources as resources
from pyyoutube.models.base import BaseModel
from pyyoutube.error import ErrorCode, ErrorMessage, PyYouTubeException
from pyyoutube.models import (
    AccessToken,
)
from pyyoutube.resources.base_resource import Resource


def _is_resource_endpoint(obj):
    return isinstance(obj, Resource)


class Client:
    """Client for YouTube resource"""

    BASE_URL = "https://www.googleapis.com/youtube/v3/"
    BASE_UPLOAD_URL = "https://www.googleapis.com/upload/youtube/v3/"
    AUTHORIZATION_URL = "https://accounts.google.com/o/oauth2/v2/auth"
    EXCHANGE_ACCESS_TOKEN_URL = "https://oauth2.googleapis.com/token"
    REVOKE_TOKEN_URL = "https://oauth2.googleapis.com/revoke"

    DEFAULT_REDIRECT_URI = "https://localhost/"
    DEFAULT_SCOPE = [
        "https://www.googleapis.com/auth/youtube",
        "https://www.googleapis.com/auth/userinfo.profile",
    ]
    DEFAULT_STATE = "Python-YouTube"

    activities = resources.ActivitiesResource()
    captions = resources.CaptionsResource()
    channels = resources.ChannelsResource()
    channelBanners = resources.ChannelBannersResource()
    channelSections = resources.ChannelSectionsResource()
    comments = resources.CommentsResource()
    commentThreads = resources.CommentThreadsResource()
    i18nLanguages = resources.I18nLanguagesResource()
    i18nRegions = resources.I18nRegionsResource()
    members = resources.MembersResource()
    membershipsLevels = resources.MembershipLevelsResource()
    playlistItems = resources.PlaylistItemsResource()
    playlists = resources.PlaylistsResource()
    search = resources.SearchResource()
    subscriptions = resources.SubscriptionsResource()
    thumbnails = resources.ThumbnailsResource()
    videoAbuseReportReasons = resources.VideoAbuseReportReasonsResource()
    videoCategories = resources.VideoCategoriesResource()
    videos = resources.VideosResource()
    watermarks = resources.WatermarksResource()

    def __new__(cls, *args, **kwargs):
        self = super().__new__(cls)
        sub_resources = inspect.getmembers(self, _is_resource_endpoint)
        for name, resource in sub_resources:
            resource_cls = type(resource)
            resource = resource_cls(self)
            setattr(self, name, resource)

        return self

    def __init__(
        self,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        access_token: Optional[str] = None,
        refresh_token: Optional[str] = None,
        api_key: Optional[str] = None,
        client_secret_path: Optional[str] = None,
        timeout: Optional[int] = None,
        proxies: Optional[dict] = None,
        headers: Optional[dict] = None,
    ) -> None:
        """Class initial

        Args:
            client_id:
                ID for your app.
            client_secret:
                Secret for your app.
            access_token:
                Access token for user authorized with your app.
            refresh_token:
                Refresh Token for user.
            api_key:
                API key for your app which generated from api console.
            client_secret_path:
                path to the client_secret.json file provided by google console
            timeout:
                Timeout for every request.
            proxies:
                Proxies for every request.
            headers:
                Headers for every request.

        Raises:
            PyYouTubeException: Missing either credentials.
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.api_key = api_key
        self.timeout = timeout
        self.proxies = proxies
        self.headers = headers

        self.session = requests.Session()
        self.merge_headers()

        if not self._has_client_data() and client_secret_path is not None:
            # try to use client_secret file
            self._from_client_secrets_file(client_secret_path)

        # Auth settings
        if not (self._has_auth_credentials() or self._has_client_data()):
            raise PyYouTubeException(
                ErrorMessage(
                    status_code=ErrorCode.MISSING_PARAMS,
                    message="Must specify either client key info or api key.",
                )
            )

    def _from_client_secrets_file(self, client_secret_path: str):
        """Set credentials from client_sectet file

        Args:
            client_secret_path:
                path to the client_secret.json file, provided by google console

        Raises:
            PyYouTubeException: missing required key, client_secret file not in 'web' format.
        """

        with open(client_secret_path, "r") as f:
            secrets_data = json.load(f)

        credentials = None
        for secrets_type in ["web", "installed"]:
            if secrets_type in secrets_data:
                credentials = secrets_data[secrets_type]

        if not credentials:
            raise PyYouTubeException(
                ErrorMessage(
                    status_code=ErrorCode.INVALID_PARAMS,
                    message="Only 'web' and 'installed' type client_secret files are supported.",
                )
            )

        # check for reqiered fields
        for field in ["client_secret", "client_id"]:
            if field not in credentials:
                raise PyYouTubeException(
                    ErrorMessage(
                        status_code=ErrorCode.MISSING_PARAMS,
                        message=f"missing required field '{field}'.",
                    )
                )

        self.client_id = credentials["client_id"]
        self.client_secret = credentials["client_secret"]

        # Set default redirect to first defined in client_secrets file if any
        if "redirect_uris" in credentials and len(credentials["redirect_uris"]) > 0:
            self.DEFAULT_REDIRECT_URI = credentials["redirect_uris"][0]

    def _has_auth_credentials(self) -> bool:
        return self.api_key or self.access_token

    def _has_client_data(self) -> bool:
        return self.client_id and self.client_secret

    def merge_headers(self):
        """Merge custom headers to session."""
        if self.headers:
            self.session.headers = merge_setting(
                request_setting=self.session.headers,
                session_setting=self.headers,
                dict_class=CaseInsensitiveDict,
            )

    @staticmethod
    def parse_response(response: Response) -> dict:
        """Response parser

        Args:
            response:
                Response from the Response.

        Returns:
            Response dict data.

        Raises:
            PyYouTubeException: If response has errors.
        """
        data = response.json()
        if "error" in data:
            raise PyYouTubeException(response)
        return data

    def request(
        self,
        path: str,
        method: str = "GET",
        params: Optional[dict] = None,
        data: Optional[dict] = None,
        json: Optional[dict] = None,
        enforce_auth: bool = True,
        is_upload: bool = False,
        **kwargs,
    ):
        """Send request to YouTube.

        Args:
            path:
                Resource or url for YouTube data. such as channels,videos and so on.
            method:
                Method for the request.
            params:
                Object to send in the query string of the request.
            data:
                Object to send in the body of the request.
            json:
                Object json to send in the body of the request.
            enforce_auth:
                Whether to use user credentials.
            is_upload:
                Whether it is an upload job.
            kwargs:
                Additional parameters for request.

        Returns:
            Response for request.

        Raises:
            PyYouTubeException: Missing credentials when need credentials.
                                Request http error.
        """
        if not path.startswith("http"):
            base_url = self.BASE_UPLOAD_URL if is_upload else self.BASE_URL
            path = base_url + path

        # Add credentials to request
        if enforce_auth:
            if self.api_key is None and self.access_token is None:
                raise PyYouTubeException(
                    ErrorMessage(
                        status_code=ErrorCode.MISSING_PARAMS,
                        message="You must provide your credentials.",
                    )
                )
            else:
                self.add_token_to_headers()
                params = self.add_api_key_to_params(params=params)

        # If json is dataclass convert to dict
        if isinstance(json, BaseModel):
            json = json.to_dict_ignore_none()

        try:
            response = self.session.request(
                method=method,
                url=path,
                params=params,
                data=data,
                json=json,
                proxies=self.proxies,
                timeout=self.timeout,
                **kwargs,
            )
        except requests.HTTPError as e:
            raise PyYouTubeException(
                ErrorMessage(status_code=ErrorCode.HTTP_ERROR, message=e.args[0])
            )
        else:
            return response

    def add_token_to_headers(self):
        if self.access_token:
            self.session.headers.update(
                {"Authorization": f"Bearer {self.access_token}"}
            )

    def add_api_key_to_params(self, params: Optional[dict] = None):
        if not self.api_key:
            return params
        if params is None:
            params = {"key": self.api_key}
        else:
            params["key"] = self.api_key
        return params

    def _get_oauth_session(
        self,
        redirect_uri: Optional[str] = None,
        scope: Optional[List[str]] = None,
        state: Optional[str] = None,
        **kwargs,
    ) -> OAuth2Session:
        """Build request session for authorization

        Args:
            redirect_uri:
                Determines how Google's authorization server sends a response to your app.
                If not provide will use default https://localhost/
            scope:
                Permission scope for authorization.
                see more: https://developers.google.com/identity/protocols/oauth2/scopes#youtube
            state:
                State sting for authorization.
            **kwargs:
                Additional parameters for session.

        Returns:
            OAuth2.0 Session
        """
        redirect_uri = (
            redirect_uri if redirect_uri is not None else self.DEFAULT_REDIRECT_URI
        )
        scope = scope if scope is not None else self.DEFAULT_SCOPE
        state = state if state is not None else self.DEFAULT_STATE

        return OAuth2Session(
            client_id=self.client_id,
            scope=scope,
            redirect_uri=redirect_uri,
            state=state,
            **kwargs,
        )

    def get_authorize_url(
        self,
        redirect_uri: Optional[str] = None,
        scope: Optional[List[str]] = None,
        access_type: str = "offline",
        state: Optional[str] = None,
        include_granted_scopes: Optional[bool] = None,
        login_hint: Optional[str] = None,
        prompt: Optional[str] = None,
        **kwargs,
    ) -> Tuple[str, str]:
        """Get authorize url for user.

        Args:
            redirect_uri:
                Determines how Google's authorization server sends a response to your app.
                If not provide will use default https://localhost/
            scope:
                The scope you want user to grant permission.
            access_type:
                Indicates whether your application can refresh access tokens when the user
                is not present at the browser.
                Valid parameter are `online` and `offline`.
            state:
                State string between your authorization request and the authorization server's response.
            include_granted_scopes:
                Enables applications to use incremental authorization to request
                access to additional scopes in context.
                Set true to enable.
            login_hint:
                Set the parameter value to an email address or sub identifier, which is
                equivalent to the user's Google ID.
            prompt:
                A space-delimited, case-sensitive list of prompts to present the user.
                Possible values are:
                - none:
                    Do not display any authentication or consent screens.
                    Must not be specified with other values.
                - consent:
                    Prompt the user for consent.
                - select_account:
                    Prompt the user to select an account.
            **kwargs:
                Additional parameters for authorize session.

        Returns:
            A tuple of (url, state)

            url: Authorize url for user.
            state: State string for authorization.

        References:
            https://developers.google.com/youtube/v3/guides/auth/server-side-web-apps
        """
        session = self._get_oauth_session(
            redirect_uri=redirect_uri,
            scope=scope,
            state=state,
            **kwargs,
        )
        authorize_url, state = session.authorization_url(
            url=self.AUTHORIZATION_URL,
            access_type=access_type,
            include_granted_scopes=include_granted_scopes,
            login_hint=login_hint,
            prompt=prompt,
        )
        return authorize_url, state

    def generate_access_token(
        self,
        authorization_response: Optional[str] = None,
        code: Optional[str] = None,
        redirect_uri: Optional[str] = None,
        scope: Optional[List[str]] = None,
        state: Optional[str] = None,
        return_json: bool = False,
        **kwargs,
    ) -> Union[dict, AccessToken]:
        """Exchange the authorization code or authorization response for an access token.

        Args:
            authorization_response:
                Response url for YouTune redirected to.
            code:
                Authorization code from authorization_response.
            redirect_uri:
                Determines how Google's authorization server sends a response to your app.
                If not provide will use default https://localhost/
            scope:
                The scope you want user to grant permission.
            state:
                State string between your authorization request and the authorization server's response.
            return_json:
                Type for returned data. If you set True JSON data will be returned.
            **kwargs:
                Additional parameters for authorize session.

        Returns:
            Access token data.
        """
        session = self._get_oauth_session(
            redirect_uri=redirect_uri,
            scope=scope,
            state=state,
            **kwargs,
        )
        token = session.fetch_token(
            token_url=self.EXCHANGE_ACCESS_TOKEN_URL,
            client_secret=self.client_secret,
            authorization_response=authorization_response,
            code=code,
            proxies=self.proxies,
        )
        self.access_token = token["access_token"]
        self.refresh_token = token.get("refresh_token")
        return token if return_json else AccessToken.from_dict(token)

    def refresh_access_token(
        self, refresh_token: str, return_json: bool = False, **kwargs
    ) -> Union[dict, AccessToken]:
        """Refresh new access token.

        Args:
            refresh_token:
                The refresh token returned from the authorization code exchange.
            return_json:
                Type for returned data. If you set True JSON data will be returned.
            **kwargs:
                Additional parameters for request.

        Returns:
            Access token data.
        """
        response = self.request(
            method="POST",
            path=self.EXCHANGE_ACCESS_TOKEN_URL,
            data={
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "refresh_token": refresh_token,
                "grant_type": "refresh_token",
            },
            enforce_auth=False,
            **kwargs,
        )
        data = self.parse_response(response)
        return data if return_json else AccessToken.from_dict(data)

    def revoke_access_token(
        self,
        token: str,
    ) -> bool:
        """Revoke token.

        Notes:
            If the token is an access token which has a corresponding refresh token,
            the refresh token will also be revoked.

        Args:
            token:
                Can be an access token or a refresh token.

        Returns:
            Revoked status

        Raises:
            PyYouTubeException: When occur errors.
        """
        response = self.request(
            method="POST",
            path=self.REVOKE_TOKEN_URL,
            params={"token": token},
            enforce_auth=False,
        )
        if response.ok:
            return True
        self.parse_response(response)
