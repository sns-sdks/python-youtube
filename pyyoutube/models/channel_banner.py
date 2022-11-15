"""
    There are channel banner related models

    References: https://developers.google.com/youtube/v3/docs/channelBanners#properties
"""

from dataclasses import dataclass, field
from typing import List, Optional

from .base import BaseModel


@dataclass
class ChannelBanner(BaseModel):
    """
    A class representing the channel banner's info.

    References: https://developers.google.com/youtube/v3/docs/channelBanners#resource
    """

    kind: Optional[str] = field(default=None)
    etag: Optional[str] = field(default=None, repr=False)
    url: Optional[str] = field(default=None)
