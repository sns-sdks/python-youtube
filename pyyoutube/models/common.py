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
        https://google-developers.appspot.com/youtube/v3/docs/videos#topicDetails.topicIds[]

    This model is customized for parsing topic id. YouTube Data Api not return this.
    """
    id: Optional[str] = field(default=None)
    description: Optional[str] = field(default=None)


@dataclass
class BaseTopicDetails(BaseModel):
    """
    This is a base model for chanel or video topic details.
    """
    topicIds: List[str] = field(default=None, repr=False)

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
    A class representing the channel or video snippet localized info.

    Refer:
        https://developers.google.com/youtube/v3/docs/channels#snippet.localized
        https://google-developers.appspot.com/youtube/v3/docs/videos#snippet.localized
    """
    title: Optional[str] = field(default=None)
    description: Optional[str] = field(default=None, repr=False)
