from dataclasses import dataclass, field
from typing import List, Optional

from .base import BaseModel


@dataclass
class AccessToken(BaseModel):
    """
    A class representing for access token.
    Refer: https://developers.google.com/youtube/v3/guides/auth/server-side-web-apps#exchange-authorization-code
    """

    access_token: Optional[str] = field(default=None)
    expires_in: Optional[int] = field(default=None)
    refresh_token: Optional[str] = field(default=None, repr=False)
    scope: Optional[List[str]] = field(default=None, repr=False)
    token_type: Optional[str] = field(default=None)
    expires_at: Optional[float] = field(default=None, repr=False)


@dataclass
class UserProfile(BaseModel):
    """
    A class representing for user profile.
    Refer: https://any-api.com/googleapis_com/oauth2/docs/userinfo/oauth2_userinfo_v2_me_get
    """

    id: Optional[str] = field(default=None)
    name: Optional[str] = field(default=None)
    given_name: Optional[str] = field(default=None, repr=False)
    family_name: Optional[str] = field(default=None, repr=False)
    picture: Optional[str] = field(default=None, repr=False)
    locale: Optional[str] = field(default=None, repr=False)
