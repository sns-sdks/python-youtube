"""
    These are playlist related models.
"""
from dataclasses import dataclass, field
from typing import Optional, List

from .base import BaseModel
from .common import BaseApiResponse, BaseResource, Localized, Player, Thumbnails
from .mixins import DatetimeTimeMixin


@dataclass
class PlaylistContentDetails(BaseModel):
    """
    A class representing playlist's content details info.

    Refer: https://developers.google.com/youtube/v3/docs/playlists#contentDetails
    """

    itemCount: Optional[int] = field(default=None)


@dataclass
class PlaylistSnippet(BaseModel, DatetimeTimeMixin):
    """
    A class representing the playlist snippet info.

    Refer: https://developers.google.com/youtube/v3/docs/playlists#snippet
    """

    publishedAt: Optional[str] = field(default=None, repr=False)
    channelId: Optional[str] = field(default=None, repr=False)
    title: Optional[str] = field(default=None)
    description: Optional[str] = field(default=None)
    thumbnails: Optional[Thumbnails] = field(default=None, repr=False)
    channelTitle: Optional[str] = field(default=None, repr=False)
    defaultLanguage: Optional[str] = field(default=None, repr=False)
    localized: Optional[Localized] = field(default=None, repr=False)


@dataclass
class PlaylistStatus(BaseModel):
    """
    A class representing the playlist status info.

    Refer: https://developers.google.com/youtube/v3/docs/playlists#status
    """

    privacyStatus: Optional[str] = field(default=None)


@dataclass
class Playlist(BaseResource):
    """
    A class representing the playlist info.

    Refer: https://developers.google.com/youtube/v3/docs/playlists
    """

    snippet: Optional[PlaylistSnippet] = field(default=None, repr=False)
    status: Optional[PlaylistStatus] = field(default=None, repr=False)
    contentDetails: Optional[PlaylistContentDetails] = field(default=None, repr=False)
    player: Optional[Player] = field(default=None, repr=False)


@dataclass
class PlaylistListResponse(BaseApiResponse):
    """
    A class representing the playlist's retrieve response info.

    Refer: https://developers.google.com/youtube/v3/docs/playlists/list#response_1
    """

    items: Optional[List[Playlist]] = field(default=None, repr=False)
