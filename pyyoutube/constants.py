import os
import httplib2

BASE_URL = "https://www.googleapis.com/youtube/v3/"
AUTHORIZATION_URL = "https://accounts.google.com/o/oauth2/v2/auth"
EXCHANGE_ACCESS_TOKEN_URL = "https://oauth2.googleapis.com/token"
USER_INFO_URL = "https://www.googleapis.com/oauth2/v1/userinfo"

DEFAULT_REDIRECT_URI = "https://localhost/"

UPLOAD_SCOPE = "https://www.googleapis.com/auth/youtube.upload"
FULL_ACCESS_SCOPE = "https://www.googleapis.com/auth/youtube"
PARTNER_SCOPE = "https://www.googleapis.com/auth/youtubepartner"
READ_WRITE_SSL_SCOPE = "https://www.googleapis.com/auth/youtube.force-ssl"

ALL_SCOPES = (
    UPLOAD_SCOPE,
    FULL_ACCESS_SCOPE,
    PARTNER_SCOPE,
    READ_WRITE_SSL_SCOPE,
)

DEFAULT_SCOPE = (
    FULL_ACCESS_SCOPE,
    "https://www.googleapis.com/auth/userinfo.profile",
)

DEFAULT_STATE = "PyYouTube"
DEFAULT_TIMEOUT = 10
DEFAULT_QUOTA = 10000  # this quota reset at 00:00:00(GMT-7) every day.
RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error, IOError)
RETRIABLE_STATUS_CODES = [500, 502, 503, 504]
DEFAULT_CLIENT_SECRETS_FILE = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "./client_secrets.json")
)

API_SERVICE_NAME = "youtube"
CURRENT_API_VERSION = "v3"

MISSING_CLIENT_SECRETS_MESSAGE = (
    """
    WARNING: Please configure OAuth 2.0
    To make this sample run you will need to populate the client_secrets.json file
    found at:
        %s
    with information from the API Console
    https://console.developers.google.com/
    For more information about the client_secrets.json file format, please visit:
    https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
    """
    % DEFAULT_CLIENT_SECRETS_FILE
)
