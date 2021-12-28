"""
    These are channel related models.
"""
from dataclasses import dataclass, field
from typing import List, Optional

from .base import BaseModel
from .common import BaseResource, BaseTopicDetails, Thumbnails, BaseApiResponse
from .mixins import DatetimeTimeMixin


@dataclass
class ChannelBrandingChannel(BaseModel):
    """
    A class representing the channel branding setting's channel info.

    Refer: https://developers.google.com/youtube/v3/docs/channels#brandingSettings.channel
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
class ChannelBrandingImage(BaseModel):
    """
    A class representing the channel branding setting's image info.

    Refer: https://developers.google.com/youtube/v3/docs/channels#brandingSettings.image
    """

    bannerImageUrl: Optional[str] = field(default=None)
    bannerMobileImageUrl: Optional[str] = field(default=None, repr=False)
    watchIconImageUrl: Optional[str] = field(default=None, repr=False)
    trackingImageUrl: Optional[str] = field(default=None, repr=False)
    bannerTabletLowImageUrl: Optional[str] = field(default=None, repr=False)
    bannerTabletImageUrl: Optional[str] = field(default=None, repr=None)
    bannerTabletHdImageUrl: Optional[str] = field(default=None, repr=None)
    bannerTabletExtraHdImageUrl: Optional[str] = field(default=None, repr=None)
    bannerMobileLowImageUrl: Optional[str] = field(default=None, repr=None)
    bannerMobileMediumHdImageUrl: Optional[str] = field(default=None, repr=None)
    bannerMobileHdImageUrl: Optional[str] = field(default=None, repr=None)
    bannerMobileExtraHdImageUrl: Optional[str] = field(default=None, repr=None)
    bannerTvImageUrl: Optional[str] = field(default=None, repr=None)
    bannerTvLowImageUrl: Optional[str] = field(default=None, repr=None)
    bannerTvMediumImageUrl: Optional[str] = field(default=None, repr=None)
    bannerTvHighImageUrl: Optional[str] = field(default=None, repr=None)
    bannerExternalUrl: Optional[str] = field(default=None, repr=None)


@dataclass
class ChannelBrandingHint(BaseModel):
    """
    A class representing the channel branding setting's hint info.

    Refer: https://developers.google.com/youtube/v3/docs/channels#brandingSettings.hints
    """

    property: Optional[str] = field(default=None)
    value: Optional[str] = field(default=None)


@dataclass
class ChannelBrandingSetting(BaseModel):
    """
    A class representing the channel branding settings info.

    Refer: https://developers.google.com/youtube/v3/docs/channels#brandingSettings
    """

    channel: Optional[ChannelBrandingChannel] = field(default=None)


@dataclass
class RelatedPlaylists(BaseModel):
    """
    A class representing the channel's related playlist info

    Refer: https://developers.google.com/youtube/v3/docs/channels#contentDetails.relatedPlaylists
    """

    likes: Optional[str] = field(default=None, repr=False)
    uploads: Optional[str] = field(default=None)


@dataclass
class ChannelContentDetails(BaseModel):
    """
    A class representing the channel's content info.

    Refer: https://developers.google.com/youtube/v3/docs/channels#contentDetails
    """

    relatedPlaylists: Optional[RelatedPlaylists] = field(default=None)


@dataclass
class ChannelTopicDetails(BaseTopicDetails):
    """
    A class representing the channel's topic detail info.

    Refer: https://developers.google.com/youtube/v3/docs/channels#topicDetails
    """

    # Important:
    # topicIds maybe has deprecated.
    # see more: https://developers.google.com/youtube/v3/revision_history#november-10-2016
    topicIds: Optional[List[str]] = field(default=None, repr=False)
    topicCategories: Optional[List[str]] = field(default=None)


@dataclass
class Localized(BaseModel):
    """
    A class representing the channel snippet localized info.

    Refer: https://developers.google.com/youtube/v3/docs/channels#snippet.localized
    """

    title: Optional[str] = field(default=None)
    description: Optional[str] = field(default=None, repr=False)


@dataclass
class ChannelSnippet(BaseModel, DatetimeTimeMixin):
    """
    A class representing the channel snippet info.

    Refer: https://developers.google.com/youtube/v3/docs/channels#snippet
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
class ChannelStatistics(BaseModel):
    """
    A class representing the Channel's statistics info.

    Refer: https://developers.google.com/youtube/v3/docs/channels#statistics
    """

    viewCount: Optional[int] = field(default=None)
    subscriberCount: Optional[int] = field(default=None)
    hiddenSubscriberCount: Optional[bool] = field(default=None, repr=False)
    videoCount: Optional[int] = field(default=None, repr=False)


@dataclass
class ChannelStatus(BaseModel):
    """
    A class representing the channel's status info.

    Refer: https://developers.google.com/youtube/v3/docs/channels#status
    """

    privacyStatus: Optional[str] = field(default=None)
    isLinked: Optional[bool] = field(default=None, repr=False)
    longUploadsStatus: Optional[str] = field(default=None, repr=False)


@dataclass
class Channel(BaseResource):
    """
    A class representing the channel's info.

    Refer: https://developers.google.com/youtube/v3/docs/channels
    """

    snippet: Optional[ChannelSnippet] = field(default=None, repr=False)
    contentDetails: Optional[ChannelContentDetails] = field(default=None, repr=False)
    statistics: Optional[ChannelStatistics] = field(default=None, repr=False)
    topicDetails: Optional[ChannelTopicDetails] = field(default=None, repr=False)
    status: Optional[ChannelStatus] = field(default=None, repr=False)
    brandingSettings: Optional[ChannelBrandingSetting] = field(default=None, repr=False)


@dataclass
class ChannelListResponse(BaseApiResponse):
    """
    A class representing the channel's retrieve response info.

    Refer: https://developers.google.com/youtube/v3/docs/channels/list#response_1
    """

    items: Optional[List[Channel]] = field(default=None, repr=False)
