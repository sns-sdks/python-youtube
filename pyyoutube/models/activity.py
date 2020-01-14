"""
    These are activity related models.
"""

from dataclasses import dataclass, field
from typing import List, Optional

from .base import BaseModel
from .common import BaseApiResponse, BaseResource, ResourceId, Thumbnails
from .mixins import DatetimeTimeMixin


@dataclass
class ActivitySnippet(BaseModel, DatetimeTimeMixin):
    """
    A class representing the activity snippet resource info.

    Refer: https://developers.google.com/youtube/v3/docs/activities#snippet
    """

    publishedAt: Optional[str] = field(default=None, repr=False)
    channelId: Optional[str] = field(default=None, repr=False)
    title: Optional[str] = field(default=None)
    description: Optional[str] = field(default=None)
    thumbnails: Optional[Thumbnails] = field(default=None, repr=False)
    channelTitle: Optional[str] = field(default=None, repr=False)
    type: Optional[str] = field(default=None, repr=False)
    groupId: Optional[str] = field(default=None, repr=False)


@dataclass
class ActivityContentDetailsUpload(BaseModel):
    """
    A class representing the activity contentDetails upload resource info.

    Refer: https://developers.google.com/youtube/v3/docs/activities#contentDetails.upload
    """

    videoId: Optional[str] = field(default=None)


@dataclass
class ActivityContentDetailsLike(BaseModel):
    """
    A class representing the activity contentDetails like resource info.

    Refer: https://developers.google.com/youtube/v3/docs/activities#contentDetails.like
    """

    resourceId: Optional[ResourceId] = field(default=None)


@dataclass
class ActivityContentDetailsFavorite(BaseModel):
    """
    A class representing the activity contentDetails favorite resource info.

    Refer: https://developers.google.com/youtube/v3/docs/activities#contentDetails.favorite
    """

    resourceId: Optional[ResourceId] = field(default=None)


@dataclass
class ActivityContentDetailsComment(BaseModel):
    """
    A class representing the activity contentDetails comment resource info.

    Refer: https://developers.google.com/youtube/v3/docs/activities#contentDetails.comment
    """

    resourceId: Optional[ResourceId] = field(default=None)


@dataclass
class ActivityContentDetailsSubscription(BaseModel):
    """
    A class representing the activity contentDetails subscription resource info.

    Refer: https://developers.google.com/youtube/v3/docs/activities#contentDetails.subscription
    """

    resourceId: Optional[ResourceId] = field(default=None)


@dataclass
class ActivityContentDetailsPlaylistItem(BaseModel):
    """
    A class representing the activity contentDetails playlistItem resource info.

    Refer: https://developers.google.com/youtube/v3/docs/activities#contentDetails.playlistItem
    """

    resourceId: Optional[ResourceId] = field(default=None)
    playlistId: Optional[str] = field(default=None)
    playlistItemId: Optional[str] = field(default=None)


@dataclass
class ActivityContentDetailsRecommendation(BaseModel):
    """
    A class representing the activity contentDetails recommendation resource info.

    Refer: https://developers.google.com/youtube/v3/docs/activities#contentDetails.recommendation
    """

    resourceId: Optional[ResourceId] = field(default=None)
    reason: Optional[str] = field(default=None)
    seedResourceId: Optional[ResourceId] = field(default=None)


@dataclass
class ActivityContentDetailsBulletin(BaseModel):
    """
    A class representing the activity contentDetails bulletin resource info.

    Refer: https://developers.google.com/youtube/v3/docs/activities#contentDetails.bulletin
    """

    resourceId: Optional[ResourceId] = field(default=None)


@dataclass
class ActivityContentDetailsSocial(BaseModel):
    """
    A class representing the activity contentDetails social resource info.

    Refer: https://developers.google.com/youtube/v3/docs/activities#contentDetails.social
    """

    resourceId: Optional[ResourceId] = field(default=None)
    type: Optional[str] = field(default=None)
    author: Optional[str] = field(default=None)
    referenceUrl: Optional[str] = field(default=None)
    imageUrl: Optional[str] = field(default=None)


@dataclass
class ActivityContentDetailsChannelItem(BaseModel):
    """
    A class representing the activity contentDetails channelItem resource info.

    Refer: https://developers.google.com/youtube/v3/docs/activities#contentDetails.channelItem
    """

    resourceId: Optional[ResourceId] = field(default=None)


@dataclass
class ActivityContentDetails(BaseModel):
    """
    A class representing the activity contentDetails resource info.

    Refer: https://developers.google.com/youtube/v3/docs/activities#contentDetails
    """

    upload: Optional[ActivityContentDetailsUpload] = field(default=None)
    like: Optional[ActivityContentDetailsLike] = field(default=None, repr=False)
    favorite: Optional[ActivityContentDetailsFavorite] = field(default=None, repr=False)
    comment: Optional[ActivityContentDetailsComment] = field(default=None, repr=False)
    subscription: Optional[ActivityContentDetailsSubscription] = field(
        default=None, repr=False
    )
    playlistItem: Optional[ActivityContentDetailsPlaylistItem] = field(
        default=None, repr=False
    )
    recommendation: Optional[ActivityContentDetailsRecommendation] = field(
        default=None, repr=False
    )
    bulletin: Optional[ActivityContentDetailsBulletin] = field(default=None, repr=False)
    social: Optional[ActivityContentDetailsSocial] = field(default=None, repr=False)
    channelItem: Optional[ActivityContentDetailsChannelItem] = field(
        default=None, repr=False
    )


@dataclass
class Activity(BaseResource):
    """
    A class representing the activity resource info.

    Refer: https://developers.google.com/youtube/v3/docs/activities
    """

    snippet: Optional[ActivitySnippet] = field(default=None)
    contentDetails: Optional[ActivityContentDetails] = field(default=None, repr=False)


@dataclass
class ActivityListResponse(BaseApiResponse):
    """
    A class representing the activity response info.

    Refer: https://developers.google.com/youtube/v3/docs/activities/list#response_1
    """

    items: Optional[List[Activity]] = field(default=None, repr=False)
