"""
    These are channel related models.

    References: https://developers.google.com/youtube/v3/docs/channels#properties
"""
from dataclasses import dataclass, field
from typing import List, Optional

from .base import BaseModel
from .common import (
    BaseResource,
    BaseTopicDetails,
    Thumbnails,
    BaseApiResponse,
    Localized,
)
from .mixins import DatetimeTimeMixin


@dataclass
class RelatedPlaylists(BaseModel):
    """
    A class representing the channel's related playlists info

    References: https://developers.google.com/youtube/v3/docs/channels#contentDetails.relatedPlaylists
    """

    likes: Optional[str] = field(default=None, repr=False)
    uploads: Optional[str] = field(default=None)


@dataclass
class ChannelBrandingSettingChannel(BaseModel):
    """
    A class representing the channel branding setting's channel info.

    References: https://developers.google.com/youtube/v3/docs/channels#brandingSettings.channel
    """

    title: Optional[str] = field(default=None)
    description: Optional[str] = field(default=None)
    keywords: Optional[str] = field(default=None, repr=False)
    trackingAnalyticsAccountId: Optional[str] = field(default=None, repr=False)
    moderateComments: Optional[bool] = field(default=None, repr=False)
    unsubscribedTrailer: Optional[str] = field(default=None, repr=False)
    defaultLanguage: Optional[str] = field(default=None, repr=False)
    country: Optional[str] = field(default=None, repr=False)


@dataclass
class ChannelBrandingSettingImage(BaseModel):
    """
    A class representing the channel branding setting's image info.

    References: https://developers.google.com/youtube/v3/docs/channels#brandingSettings.image
    """

    bannerExternalUrl: Optional[str] = field(default=None, repr=False)


@dataclass
class ChannelSnippet(BaseModel, DatetimeTimeMixin):
    """
    A class representing the channel snippet info.

    References: https://developers.google.com/youtube/v3/docs/channels#snippet
    """

    title: Optional[str] = field(default=None)
    description: Optional[str] = field(default=None)
    customUrl: Optional[str] = field(default=None, repr=False)
    publishedAt: Optional[str] = field(default=None, repr=False)
    thumbnails: Optional[Thumbnails] = field(default=None, repr=False)
    defaultLanguage: Optional[str] = field(default=None, repr=False)
    localized: Optional[Localized] = field(default=None, repr=False)
    country: Optional[str] = field(default=None, repr=False)


@dataclass
class ChannelContentDetails(BaseModel):
    """
    A class representing the channel's content info.

    References: https://developers.google.com/youtube/v3/docs/channels#contentDetails
    """

    relatedPlaylists: Optional[RelatedPlaylists] = field(default=None)


@dataclass
class ChannelStatistics(BaseModel):
    """
    A class representing the Channel's statistics info.

    References: https://developers.google.com/youtube/v3/docs/channels#statistics
    """

    viewCount: Optional[int] = field(default=None)
    subscriberCount: Optional[int] = field(default=None)
    hiddenSubscriberCount: Optional[bool] = field(default=None, repr=False)
    videoCount: Optional[int] = field(default=None, repr=False)


@dataclass
class ChannelTopicDetails(BaseTopicDetails):
    """
    A class representing the channel's topic detail info.

    References: https://developers.google.com/youtube/v3/docs/channels#topicDetails
    """

    # Important:
    # topicIds maybe has deprecated.
    # see more: https://developers.google.com/youtube/v3/revision_history#november-10-2016
    topicIds: Optional[List[str]] = field(default=None, repr=False)
    topicCategories: Optional[List[str]] = field(default=None)


@dataclass
class ChannelStatus(BaseModel):
    """
    A class representing the channel's status info.

    References: https://developers.google.com/youtube/v3/docs/channels#status
    """

    privacyStatus: Optional[str] = field(default=None)
    isLinked: Optional[bool] = field(default=None, repr=False)
    longUploadsStatus: Optional[str] = field(default=None, repr=False)
    madeForKids: Optional[bool] = field(default=None, repr=False)
    selfDeclaredMadeForKids: Optional[bool] = field(default=None, repr=False)


@dataclass
class ChannelBrandingSetting(BaseModel):
    """
    A class representing the channel branding settings info.

    References: https://developers.google.com/youtube/v3/docs/channels#brandingSettings
    """

    channel: Optional[ChannelBrandingSettingChannel] = field(default=None)
    image: Optional[ChannelBrandingSettingImage] = field(default=None)


@dataclass
class ChannelAuditDetails(BaseModel):
    """A class representing the channel audit details info.

    References: https://developers.google.com/youtube/v3/docs/channels#auditDetails
    """

    overallGoodStanding: Optional[bool] = field(default=None)
    communityGuidelinesGoodStanding: Optional[bool] = field(default=None, repr=True)
    copyrightStrikesGoodStanding: Optional[bool] = field(default=None, repr=True)
    contentIdClaimsGoodStanding: Optional[bool] = field(default=None, repr=True)


@dataclass
class ChannelContentOwnerDetails(BaseModel):
    """A class representing the channel data relevant for YouTube Partners.

    References: https://developers.google.com/youtube/v3/docs/channels#contentOwnerDetails
    """

    contentOwner: Optional[str] = field(default=None)
    timeLinked: Optional[str] = field(default=None)


@dataclass
class Channel(BaseResource):
    """
    A class representing the channel's info.

    References: https://developers.google.com/youtube/v3/docs/channels
    """

    snippet: Optional[ChannelSnippet] = field(default=None, repr=False)
    contentDetails: Optional[ChannelContentDetails] = field(default=None, repr=False)
    statistics: Optional[ChannelStatistics] = field(default=None, repr=False)
    topicDetails: Optional[ChannelTopicDetails] = field(default=None, repr=False)
    status: Optional[ChannelStatus] = field(default=None, repr=False)
    brandingSettings: Optional[ChannelBrandingSetting] = field(default=None, repr=False)
    auditDetails: Optional[ChannelAuditDetails] = field(default=None, repr=False)
    contentOwnerDetails: Optional[ChannelContentOwnerDetails] = field(
        default=None, repr=False
    )
    localizations: Optional[dict] = field(default=None, repr=False)


@dataclass
class ChannelListResponse(BaseApiResponse):
    """
    A class representing the channel's retrieve response info.

    References: https://developers.google.com/youtube/v3/docs/channels/list#response
    """

    items: Optional[List[Channel]] = field(default=None, repr=False)
