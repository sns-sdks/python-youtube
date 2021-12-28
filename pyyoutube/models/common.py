"""
    These are common models for multi resource.
"""
from dataclasses import dataclass, field
from typing import Optional, List

from .base import BaseModel


@dataclass
class Thumbnail(BaseModel):
    """
    A class representing the thumbnail resource info.

    Refer: https://developers.google.com/youtube/v3/docs/channels#snippet.thumbnails.(key).url
    """

    url: Optional[str] = field(default=None)
    width: Optional[int] = field(default=None, repr=False)
    height: Optional[int] = field(default=None, repr=False)


@dataclass
class Thumbnails(BaseModel):
    """
    A class representing the multi thumbnail resource info.

    Refer: https://developers.google.com/youtube/v3/docs/channels#snippet.thumbnails
    """

    default: Optional[Thumbnail] = field(default=None)
    medium: Optional[Thumbnail] = field(default=None, repr=False)
    high: Optional[Thumbnail] = field(default=None, repr=False)
    standard: Optional[Thumbnail] = field(default=None, repr=False)
    maxres: Optional[Thumbnail] = field(default=None, repr=False)


@dataclass
class Topic(BaseModel):
    """
    A class representing the channel topic info. this model also suitable for video.

    Refer:
        https://developers.google.com/youtube/v3/docs/channels#topicDetails.topicIds[]
        https://developers.google.com/youtube/v3/docs/videos#topicDetails.topicIds[]

    This model is customized for parsing topic id. YouTube Data Api not return this.
    """

    id: Optional[str] = field(default=None)
    description: Optional[str] = field(default=None)


@dataclass
class BaseTopicDetails(BaseModel):
    """
    This is the base model for channel or video topic details.
    """

    topicIds: List[str] = field(default=None, repr=False)

    def get_full_topics(self):
        """
        Convert topicIds list to Topic model list
        :return: List[Topic]
        """
        from pyyoutube import TOPICS

        r: List[Topic] = []
        if self.topicIds:
            for topic_id in self.topicIds:
                topic = Topic.from_dict(
                    {"id": topic_id, "description": TOPICS.get(topic_id)}
                )
                r.append(topic)
        return r


@dataclass
class Localized(BaseModel):
    """
    A class representing the channel or video snippet localized info.

    Refer:
        https://developers.google.com/youtube/v3/docs/channels#snippet.localized
        https://developers.google.com/youtube/v3/docs/videos#snippet.localized
    """

    title: Optional[str] = field(default=None)
    description: Optional[str] = field(default=None, repr=False)


@dataclass
class PageInfo(BaseModel):
    """
    This is data model for save paging data.
    Note:
        totalResults is only an approximation/estimate.
        Refer:
            https://stackoverflow.com/questions/43507281/totalresults-count-doesnt-match-with-the-actual-results-returned-in-youtube-v3
    """

    totalResults: Optional[int] = field(default=None)
    resultsPerPage: Optional[int] = field(default=None)


@dataclass
class BaseApiResponse(BaseModel):
    """
    This is Data Api response structure when retrieve data.
    They both have same response structure, but items.

    Refer:
        https://developers.google.com/youtube/v3/docs/channels/list#response_1
        https://developers.google.com/youtube/v3/docs/playlistItems/list#response_1
    """

    kind: Optional[str] = field(default=None)
    etag: Optional[str] = field(default=None, repr=False)
    nextPageToken: Optional[str] = field(default=None, repr=False)
    prevPageToken: Optional[str] = field(default=None, repr=False)
    pageInfo: Optional[PageInfo] = field(default=None, repr=False)


@dataclass
class BaseResource(BaseModel):
    """
    This is a base model for different resource type.

    Refer: https://developers.google.com/youtube/v3/docs#resource-types
    """

    kind: Optional[str] = field(default=None)
    etag: Optional[str] = field(default=None, repr=False)
    id: Optional[str] = field(default=None)


@dataclass
class ResourceId(BaseModel):
    """
    A class representing the subscription snippet resource info.
    Refer:
        1. https://developers.google.com/youtube/v3/docs/playlistItems#snippet.resourceId
        2. https://developers.google.com/youtube/v3/docs/subscriptions#snippet.resourceId
        3. https://developers.google.com/youtube/v3/docs/activities#contentDetails.social.resourceId
    """

    kind: Optional[str] = field(default=None)
    videoId: Optional[str] = field(default=None)
    channelId: Optional[str] = field(default=None)
    playlistId: Optional[str] = field(default=None)


@dataclass
class Player(BaseModel):
    """
    A class representing the video,playlist player info.

    Refer:
        https://developers.google.com/youtube/v3/docs/videos#player

    """

    embedHtml: Optional[str] = field(default=None)
    # Important:
    # follows attributions maybe not exists.
    embedHeight: Optional[int] = field(default=None, repr=False)
    embedWidth: Optional[int] = field(default=None, repr=False)
