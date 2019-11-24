"""
    These are common models for multi resource.
"""
import datetime
from dataclasses import dataclass, field
from typing import Optional, List

from .base import BaseModel


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
class TopicDetails(BaseModel):
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
class Snippet(BaseModel):
    """
    This is a base model for chanel or video snippet.
    """
    publishedAt: Optional[str] = field(default=None, repr=False)

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
class Localized(BaseModel):
    """
    A class representing the channel or video snippet localized info.

    Refer:
        https://developers.google.com/youtube/v3/docs/channels#snippet.localized
        https://google-developers.appspot.com/youtube/v3/docs/videos#snippet.localized
    """
    title: Optional[str] = field(default=None)
    description: Optional[str] = field(default=None, repr=False)
