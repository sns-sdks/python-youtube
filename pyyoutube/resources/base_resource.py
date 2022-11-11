"""
    Base resource class.
"""
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from pyyoutube import Client  # pragma: no cover


class Resource:
    """Resource base class"""

    def __init__(self, client: Optional["Client"] = None):
        self._client = client

    @property
    def access_token(self):
        return self._client.access_token

    @property
    def api_key(self):
        return self._client.api_key
