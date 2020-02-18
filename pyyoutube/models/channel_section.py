"""
    Those are models related to channel sections.
"""

from dataclasses import dataclass, field, make_dataclass
from typing import Dict, List, Optional

from .base import BaseModel
from .common import Localized, BaseResource, BaseApiResponse


@dataclass
class ChannelSectionSnippet(BaseModel):
    """
    A class representing the channel section snippet info.

    Refer: https://developers.google.com/youtube/v3/docs/channelSections#snippet
    """
    type: Optional[str] = field(default=None)
    style: Optional[str] = field(default=None, repr=False)
    channelId: Optional[str] = field(default=None, repr=False)
    title: Optional[str] = field(default=None, repr=False)
    position: Optional[int] = field(default=None)
    defaultLanguage: Optional[str] = field(default=None, repr=False)
    localized: Optional[Localized] = field(default=None, repr=False)


@dataclass
class ChannelSectionContentDetails(BaseModel):
    """
    A class representing the channel section content details info.

    Refer: https://developers.google.com/youtube/v3/docs/channelSections#contentDetails
    """
    playlists: Optional[List[str]] = field(default=None, repr=False)
    channels: Optional[List[str]] = field(default=None)


@dataclass
class ChannelSectionLocalizationsBase(BaseModel):
    """
    A class representing the channel section localizations info.

    Refer: https://developers.google.com/youtube/v3/docs/channelSections#contentDetails
    """


@dataclass
class ChannelSectionTargeting(BaseModel):
    """
    A class representing the channel section targeting info.

    Refer: https://developers.google.com/youtube/v3/docs/channelSections#contentDetails
    """
    languages: Optional[List[str]] = field(default=None)
    regions: Optional[List[str]] = field(default=None, repr=False)
    countries: Optional[List[str]] = field(default=None, repr=False)


@dataclass
class ChannelSection(BaseResource):
    """
    A class representing the channel section info.

    Refer: https://developers.google.com/youtube/v3/docs/channelSections
    """

    snippet: Optional[ChannelSectionSnippet] = field(default=None, repr=False)
    contentDetails: Optional[ChannelSectionContentDetails] = field(default=None, repr=False)
    localizations: Optional[Dict] = field(default=None, repr=False)
    targeting: Optional[ChannelSectionTargeting] = field(default=None, repr=False)

    def __post_init__(self):
        if self.localizations is not None:
            localizations = make_dataclass(
                "ChannelSectionLocalizations",
                [
                    (key, Optional[Localized], field(default=None, repr=False))
                    for key in self.localizations.keys()
                ],
                bases=BaseModel,
            )
            return localizations.from_dict(self.localizations)
