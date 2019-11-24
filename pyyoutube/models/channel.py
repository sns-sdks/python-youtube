"""
    These are channel related models.
"""
import datetime
from dataclasses import dataclass, field
from typing import List, Optional

from .base import BaseModel
from .image import Thumbnails


@dataclass
class ChannelBrandingChannel(BaseModel):
    """
    A class representing the channel branding setting's channel info.
    Refer: https://developers.google.com/youtube/v3/docs/channels#brandingSettings.channel
    """
    title: Optional[str] = field(default=None)
    description: Optional[str] = field(default=None)
    keywords: Optional[str] = field(default=None, repr=False)
    defaultTab: Optional[str] = field(default=None, repr=False)
    trackingAnalyticsAccountId: Optional[str] = field(default=None, repr=False)
    moderateComments: Optional[bool] = field(default=None, repr=False)
    showRelatedChannels: Optional[bool] = field(default=None, repr=False)
    showBrowseView: Optional[bool] = field(default=None, repr=False)
    featuredChannelsTitle: Optional[str] = field(default=None, repr=False)
    featuredChannelsUrls: List[str] = field(default=None, repr=False)
    unsubscribedTrailer: Optional[str] = field(default=None, repr=False)
    profileColor: Optional[str] = field(default=None, repr=False)
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
    image: Optional[ChannelBrandingImage] = field(default=None)
    hints: List[ChannelBrandingHint] = field(default=None, repr=False)


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
class Topic(BaseModel):
    """
    A class representing the channel topic info.
    Refer: https://developers.google.com/youtube/v3/docs/channels#topicDetails.topicIds[]

    This model is customized for parsing topic id. YouTube Data Api not return this.
    """
    id: Optional[str] = field(default=None)
    description: Optional[str] = field(default=None)


@dataclass
class ChannelTopicDetails(BaseModel):
    """
    A class representing the channel's topic detail info.
    Refer: https://developers.google.com/youtube/v3/docs/channels#topicDetails
    """
    # Important:
    # topicIds maybe has deprecated.
    # see more: https://google-developers.appspot.com/youtube/v3/revision_history#november-10-2016
    topicIds: List[str] = field(default=None, repr=False)
    topicCategories: List[str] = field(default=None)

    def get_full_topics(self):
        """
        Convert topicIds list to Topic model list
        :return: List[Topic]
        """
        from pyyoutube import CHANNEL_TOPICS
        r: List[Topic] = []
        if self.topicIds:
            for topic_id in self.topicIds:
                topic = Topic.from_dict({
                    "id": topic_id,
                    "description": CHANNEL_TOPICS.get(topic_id)
                })
                r.append(topic)
        return r


@dataclass
class Localized(BaseModel):
    """
    A class representing the channel snippet localized info.
    Refer: https://developers.google.com/youtube/v3/docs/channels#snippet.localized
    """
    title: Optional[str] = field(default=None)
    description: Optional[str] = field(default=None, repr=False)


@dataclass
class ChannelSnippet(BaseModel):
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

    def published_at_to_datetime(self) -> Optional[datetime.datetime]:
        """
        Convert publishedAt string to datetime instance.
        original string format is YYYY-MM-DDThh:mm:ss.sZ.
        :return:
        """
        if not self.publishedAt:
            return None
        try:
            published_at = self.publishedAt.replace('Z', '+00:00')
            r = datetime.datetime.fromisoformat(published_at)
        except TypeError:
            raise
        else:
            return r


@dataclass
class ChannelStatistics(BaseModel):
    """
    A class representing the Channel's statistics info.
    Refer: https://developers.google.com/youtube/v3/docs/channels#statistics
    """
    viewCount: Optional[int] = field(default=None)
    commentCount: Optional[int] = field(default=None, repr=False)
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
class Channel(BaseModel):
    """
    A class representing the channel's info.
    Refer: https://developers.google.com/youtube/v3/docs/channels
    """
    kind: Optional[str] = field(default=None)
    etag: Optional[str] = field(default=None, repr=False)
    id: Optional[str] = field(default=None)
    snippet: Optional[ChannelSnippet] = field(default=None, repr=False)
    contentDetails: Optional[ChannelContentDetails] = field(default=None, repr=False)
    statistics: Optional[ChannelStatistics] = field(default=None, repr=False)
    topicDetails: Optional[ChannelTopicDetails] = field(default=None, repr=False)
    status: Optional[ChannelStatus] = field(default=None, repr=False)
    brandingSettings: Optional[ChannelBrandingSetting] = field(default=None, repr=False)
