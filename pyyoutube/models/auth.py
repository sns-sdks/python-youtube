from dataclasses import dataclass, field
from typing import List

from .base import BaseModel


@dataclass
class AccessToken(BaseModel):
    """
    A class representing for access token.
    Refer: https://developers.google.com/youtube/v3/guides/auth/installed-apps#obtainingaccesstokens
    """

    access_token: str = field(default=None)
    expires_in: int = field(default=None)
    refresh_token: str = field(default=None, repr=False)
    scope: List[str] = field(default=None, repr=False)
    token_type: str = field(default=None)
    id_token: str = field(default=None, repr=False)


@dataclass
class UserProfile(BaseModel):
    """
    A class representing for user profile.
    Refer: https://any-api.com/googleapis_com/oauth2/docs/userinfo/oauth2_userinfo_v2_me_get
    """

    id: str = field(default=None)
    name: str = field(default=None)
    given_name: str = field(default=None, repr=False)
    family_name: str = field(default=None, repr=False)
    picture: str = field(default=None, repr=False)
    locale: str = field(default=None, repr=False)
