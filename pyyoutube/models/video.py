"""
    These are video related models.
"""
from dataclasses import dataclass, field
from typing import Optional, List

import isodate
from isodate import ISO8601Error

from pyyoutube.error import ErrorCode, ErrorMessage, PyYouTubeException
from .base import BaseModel
from .common import (
    BaseApiResponse,
    BaseTopicDetails,
    BaseResource,
    Localized,
    Player,
    Thumbnails,
)
from .mixins import DatetimeTimeMixin


@dataclass
class RegionRestriction(BaseModel):
    """
    A class representing the video content details region restriction info

    Refer: https://developers.google.com/youtube/v3/docs/videos#contentDetails.regionRestriction
    """

    allowed: List[str] = field(default=None)
    blocked: List[str] = field(default=None, repr=False)


# TODO get detail rating description
class ContentRating(BaseModel):
    """
    A class representing the video content rating info.

    Refer: https://developers.google.com/youtube/v3/docs/videos#contentDetails.contentRating
    """

    acbRating: Optional[str] = field(default=None, repr=False)
    agcomRating: Optional[str] = field(default=None, repr=False)
    anatelRating: Optional[str] = field(default=None, repr=False)
    bbfcRating: Optional[str] = field(default=None, repr=False)
    bfvcRating: Optional[str] = field(default=None, repr=False)
    bmukkRating: Optional[str] = field(default=None, repr=False)
    catvRating: Optional[str] = field(default=None, repr=False)
    catvfrRating: Optional[str] = field(default=None, repr=False)
    cbfcRating: Optional[str] = field(default=None, repr=False)
    cccRating: Optional[str] = field(default=None, repr=False)
    cceRating: Optional[str] = field(default=None, repr=False)
    chfilmRating: Optional[str] = field(default=None, repr=False)
    chvrsRating: Optional[str] = field(default=None, repr=False)
    cicfRating: Optional[str] = field(default=None, repr=False)
    cnaRating: Optional[str] = field(default=None, repr=False)
    cncRating: Optional[str] = field(default=None, repr=False)
    csaRating: Optional[str] = field(default=None, repr=False)
    cscfRating: Optional[str] = field(default=None, repr=False)
    czfilmRating: Optional[str] = field(default=None, repr=False)
    djctqRating: Optional[str] = field(default=None, repr=False)
    djctqRatingReasons: List[str] = field(default=None, repr=False)
    ecbmctRating: Optional[str] = field(default=None, repr=False)
    eefilmRating: Optional[str] = field(default=None, repr=False)
    egfilmRating: Optional[str] = field(default=None, repr=False)
    eirinRating: Optional[str] = field(default=None, repr=False)
    fcbmRating: Optional[str] = field(default=None, repr=False)
    fcoRating: Optional[str] = field(default=None, repr=False)
    fpbRating: Optional[str] = field(default=None, repr=False)
    fpbRatingReasons: List[str] = field(default=None, repr=False)
    fskRating: Optional[str] = field(default=None, repr=False)
    grfilmRating: Optional[str] = field(default=None, repr=False)
    icaaRating: Optional[str] = field(default=None, repr=False)
    ifcoRating: Optional[str] = field(default=None, repr=False)
    ilfilmRating: Optional[str] = field(default=None, repr=False)
    incaaRating: Optional[str] = field(default=None, repr=False)
    kfcbRating: Optional[str] = field(default=None, repr=False)
    kijkwijzerRating: Optional[str] = field(default=None, repr=False)
    kmrbRating: Optional[str] = field(default=None, repr=False)
    lsfRating: Optional[str] = field(default=None, repr=False)
    mccaaRating: Optional[str] = field(default=None, repr=False)
    mccypRating: Optional[str] = field(default=None, repr=False)
    mcstRating: Optional[str] = field(default=None, repr=False)
    mdaRating: Optional[str] = field(default=None, repr=False)
    medietilsynetRating: Optional[str] = field(default=None, repr=False)
    mekuRating: Optional[str] = field(default=None, repr=False)
    mibacRating: Optional[str] = field(default=None, repr=False)
    mocRating: Optional[str] = field(default=None, repr=False)
    moctwRating: Optional[str] = field(default=None, repr=False)
    mpaaRating: Optional[str] = field(default=None, repr=False)
    mpaatRating: Optional[str] = field(default=None, repr=False)
    mtrcbRating: Optional[str] = field(default=None, repr=False)
    nbcRating: Optional[str] = field(default=None, repr=False)
    nfrcRating: Optional[str] = field(default=None, repr=False)
    nfvcbRating: Optional[str] = field(default=None, repr=False)
    nkclvRating: Optional[str] = field(default=None, repr=False)
    oflcRating: Optional[str] = field(default=None, repr=False)
    pefilmRating: Optional[str] = field(default=None, repr=False)
    resorteviolenciaRating: Optional[str] = field(default=None, repr=False)
    rtcRating: Optional[str] = field(default=None, repr=False)
    rteRating: Optional[str] = field(default=None, repr=False)
    russiaRating: Optional[str] = field(default=None, repr=False)
    skfilmRating: Optional[str] = field(default=None, repr=False)
    smaisRating: Optional[str] = field(default=None, repr=False)
    smsaRating: Optional[str] = field(default=None, repr=False)
    tvpgRating: Optional[str] = field(default=None, repr=False)
    ytRating: Optional[str] = field(default=None)


@dataclass
class VideoContentDetails(BaseModel):
    """
    A class representing the video content details info.

    Refer: https://developers.google.com/youtube/v3/docs/videos#contentDetails
    """

    duration: Optional[str] = field(default=None)
    dimension: Optional[str] = field(default=None)
    definition: Optional[str] = field(default=None, repr=False)
    caption: Optional[str] = field(default=None, repr=False)
    licensedContent: Optional[bool] = field(default=None, repr=False)
    regionRestriction: Optional[RegionRestriction] = field(default=None, repr=False)
    contentRating: Optional[ContentRating] = field(default=None, repr=False)
    projection: Optional[str] = field(default=None, repr=False)
    hasCustomThumbnail: Optional[bool] = field(default=None, repr=False)

    def get_video_seconds_duration(self):
        if not self.duration:
            return None
        try:
            seconds = isodate.parse_duration(self.duration).total_seconds()
        except ISO8601Error as e:
            raise PyYouTubeException(
                ErrorMessage(status_code=ErrorCode.INVALID_PARAMS, message=e.args[0])
            )
        else:
            return int(seconds)


@dataclass
class VideoTopicDetails(BaseTopicDetails):
    """
    A class representing video's topic detail info.

    Refer: https://developers.google.com/youtube/v3/docs/videos#topicDetails
    """

    # Important:
    # This property has been deprecated as of November 10, 2016.
    # Any topics associated with a video are now returned by the topicDetails.relevantTopicIds[] property value.
    topicIds: Optional[List[str]] = field(default=None, repr=False)
    relevantTopicIds: Optional[List[str]] = field(default=None, repr=False)
    topicCategories: Optional[List[str]] = field(default=None)

    def __post_init__(self):
        """
        If topicIds is not return and relevantTopicIds has return. let relevantTopicIds for topicIds.
        This is for the get_full_topics method.
        :return:
        """
        if self.topicIds is None and self.relevantTopicIds is not None:
            self.topicIds = self.relevantTopicIds


@dataclass
class VideoSnippet(BaseModel, DatetimeTimeMixin):
    """
    A class representing the video snippet info.

    Refer: https://developers.google.com/youtube/v3/docs/videos#snippet
    """

    publishedAt: Optional[str] = field(default=None, repr=False)
    channelId: Optional[str] = field(default=None, repr=False)
    title: Optional[str] = field(default=None)
    description: Optional[str] = field(default=None)
    thumbnails: Optional[Thumbnails] = field(default=None, repr=False)
    channelTitle: Optional[str] = field(default=None, repr=False)
    tags: Optional[List[str]] = field(default=None, repr=False)
    categoryId: Optional[str] = field(default=None, repr=False)
    liveBroadcastContent: Optional[str] = field(default=None, repr=False)
    defaultLanguage: Optional[str] = field(default=None, repr=False)
    localized: Optional[Localized] = field(default=None, repr=False)
    defaultAudioLanguage: Optional[str] = field(default=None, repr=False)


@dataclass
class VideoStatistics(BaseModel):
    """
    A class representing the video statistics info.

    Refer: https://developers.google.com/youtube/v3/docs/videos#statistics
    """

    viewCount: Optional[int] = field(default=None)
    likeCount: Optional[int] = field(default=None)
    dislikeCount: Optional[int] = field(default=None, repr=False)
    commentCount: Optional[int] = field(default=None, repr=False)


@dataclass
class VideoStatus(BaseModel, DatetimeTimeMixin):
    """
    A class representing the video status info.

    Refer: https://developers.google.com/youtube/v3/docs/videos#status
    """

    uploadStatus: Optional[str] = field(default=None)
    failureReason: Optional[str] = field(default=None, repr=False)
    rejectionReason: Optional[str] = field(default=None, repr=False)
    privacyStatus: Optional[str] = field(default=None)
    publishAt: Optional[str] = field(default=None, repr=False)
    license: Optional[str] = field(default=None, repr=False)
    embeddable: Optional[bool] = field(default=None, repr=False)
    publicStatsViewable: Optional[bool] = field(default=None, repr=False)
    madeForKids: Optional[bool] = field(default=None, repr=False)
    selfDeclaredMadeForKids: Optional[bool] = field(default=None, repr=False)


@dataclass
class VideoLiveStreamingDetails(BaseModel, DatetimeTimeMixin):
    """
    A class representing the video live streaming details.

    Refer: https://developers.google.com/youtube/v3/docs/videos#liveStreamingDetails
    """

    actualStartTime: Optional[str] = field(default=None, repr=False)
    actualEndTime: Optional[str] = field(default=None, repr=False)
    scheduledStartTime: Optional[str] = field(default=None, repr=False)
    scheduledEndTime: Optional[str] = field(default=None, repr=False)
    concurrentViewers: Optional[int] = field(default=None)
    activeLiveChatId: Optional[str] = field(default=None, repr=False)


@dataclass
class Video(BaseResource):
    """
    A class representing the video info.

    Refer: https://developers.google.com/youtube/v3/docs/videos
    """

    snippet: Optional[VideoSnippet] = field(default=None, repr=False)
    contentDetails: Optional[VideoContentDetails] = field(default=None, repr=False)
    status: Optional[VideoStatus] = field(default=None, repr=False)
    statistics: Optional[VideoStatistics] = field(default=None, repr=False)
    topicDetails: Optional[VideoTopicDetails] = field(default=None, repr=False)
    player: Optional[Player] = field(default=None, repr=False)
    liveStreamingDetails: Optional[VideoLiveStreamingDetails] = field(
        default=None, repr=False
    )


@dataclass
class VideoListResponse(BaseApiResponse):
    """
    A class representing the video's retrieve response info.

    Refer: https://developers.google.com/youtube/v3/docs/videos/list#response_1
    """

    items: Optional[List[Video]] = field(default=None, repr=False)
