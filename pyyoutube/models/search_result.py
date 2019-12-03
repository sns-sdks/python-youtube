"""
    These are search result related models.
"""
from dataclasses import dataclass, field
from typing import Optional, List

from .base import BaseModel
from .common import BaseApiResponse, BaseResource, Thumbnails
from .mixins import DatetimeTimeMixin


@dataclass
class SearchResultSnippet(BaseModel, DatetimeTimeMixin):
    """
    A class representing the search result snippet info.

    Refer: https://developers.google.com/youtube/v3/docs/search#snippet
    """

    publishedAt: Optional[str] = field(default=None, repr=False)
    channelId: Optional[str] = field(default=None)
    title: Optional[str] = field(default=None)
    description: Optional[str] = field(default=None, repr=False)
    thumbnails: Optional[Thumbnails] = field(default=None, repr=False)
    channelTitle: Optional[str] = field(default=None, repr=False)
    liveBroadcastContent: Optional[str] = field(default=None, repr=False)


@dataclass
class SearchResultId(BaseModel):
    """
    A class representing the search result id info.

    Refer: https://developers.google.com/youtube/v3/docs/search#id
    """

    kind: Optional[str] = field(default=None)
    videoId: Optional[str] = field(default=None, repr=False)
    channelId: Optional[str] = field(default=None, repr=False)
    playlistId: Optional[str] = field(default=None, repr=False)


@dataclass
class SearchResult(BaseResource):
    """
    A class representing the search result's info.

    Refer: https://developers.google.com/youtube/v3/docs/search
    """

    id: Optional[SearchResultId] = field(default=None, repr=False)
    snippet: Optional[SearchResultSnippet] = field(default=None, repr=False)


@dataclass
class SearchListResponse(BaseApiResponse):
    """
    A class representing the channel's retrieve response info.

    Refer: https://developers.google.com/youtube/v3/docs/channels/list#response_1
    """

    regionCode: Optional[str] = field(default=None, repr=False)
    items: Optional[List[SearchResult]] = field(default=None, repr=False)
