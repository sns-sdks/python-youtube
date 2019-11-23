from .base import BaseModel


class AccessToken(BaseModel):
    """
    A class representing access toke for api.
    Refer: https://developers.google.com/youtube/v3/guides/auth/installed-apps#obtainingaccesstokens
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.param_defaults = {
            'access_token': None,
            'expires_in': None,
            'refresh_token': None,
            'scope': None,  # Refer: https://developers.google.com/identity/protocols/googlescopes
            'token_type': None,
            'id_token': None
        }
        self.initial(kwargs)

    def __repr__(self):
        return f"AccessToken(access_token={self.access_token}, expires_in={self.expires_in})"


class UserProfile(BaseModel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.param_defaults = {
            'id': None,
            'name': None,
            'given_name': None,
            'family_name': None,
            'picture': None,
            'locale': None
        }
        self.initial(kwargs)

    def __repr__(self):
        return f"User(id={self.id}, name={self.name})"
