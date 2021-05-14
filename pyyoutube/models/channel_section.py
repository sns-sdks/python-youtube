"""
    Those are models related to channel sections.
"""

from dataclasses import dataclass, field, make_dataclass
from dataclasses_json import config
from typing import List, Optional, Any

from .base import BaseModel
from .common import Localized, BaseResource, BaseApiResponse


@dataclass
class ChannelSectionSnippet(BaseModel):
    """
    A class representing the channel section snippet info.

    Refer: https://developers.google.com/youtube/v3/docs/channelSections#snippet
    """

    type: Optional[str] = field(default=None)
    channelId: Optional[str] = field(default=None, repr=False)
    title: Optional[str] = field(default=None, repr=False)
    position: Optional[int] = field(default=None)


@dataclass
class ChannelSectionContentDetails(BaseModel):
    """
    A class representing the channel section content details info.

    Refer: https://developers.google.com/youtube/v3/docs/channelSections#contentDetails
    """

    playlists: Optional[List[str]] = field(default=None, repr=False)
    channels: Optional[List[str]] = field(default=None)


@dataclass
class ChannelSection(BaseResource):
    """
    A class representing the channel section info.

    Refer: https://developers.google.com/youtube/v3/docs/channelSections
    """

    snippet: Optional[ChannelSectionSnippet] = field(default=None, repr=False)
    contentDetails: Optional[ChannelSectionContentDetails] = field(
        default=None, repr=False
    )


@dataclass
class ChannelSectionResponse(BaseApiResponse):
    """
    A class representing the channel section's retrieve response info.

    Refer: https://developers.google.com/youtube/v3/docs/channelSections/list?#properties_1
    """

    items: Optional[List[ChannelSection]] = field(default=None, repr=False)
