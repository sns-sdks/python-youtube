"""
    These are comment related models.
"""

from dataclasses import dataclass, field
from typing import List, Optional

from .base import BaseModel
from .mixins import DatetimeTimeMixin
from .common import BaseApiResponse, BaseResource


@dataclass
class CommentSnippetAuthorChannelId(BaseModel):
    """
    A class representing comment's snippet authorChannelId info.

    Refer: https://developers.google.com/youtube/v3/docs/comments#snippet.authorChannelId
    """

    value: Optional[str] = field(default=None)


@dataclass
class CommentSnippet(BaseModel, DatetimeTimeMixin):
    """
    A class representing comment's snippet info.

    Refer: https://developers.google.com/youtube/v3/docs/comments#snippet
    """

    authorDisplayName: Optional[str] = field(default=None)
    authorProfileImageUrl: Optional[str] = field(default=None, repr=False)
    authorChannelUrl: Optional[str] = field(default=None, repr=False)
    authorChannelId: Optional[CommentSnippetAuthorChannelId] = field(
        default=None, repr=False
    )
    channelId: Optional[str] = field(default=None, repr=False)
    # videoId has deprecated, see https://developers.google.com/youtube/v3/revision_history#november-09,-2023
    videoId: Optional[str] = field(default=None, repr=False)
    textDisplay: Optional[str] = field(default=None, repr=False)
    textOriginal: Optional[str] = field(default=None, repr=False)
    parentId: Optional[str] = field(default=None, repr=False)
    canRate: Optional[bool] = field(default=None, repr=False)
    viewerRating: Optional[str] = field(default=None, repr=False)
    likeCount: Optional[int] = field(default=None)
    moderationStatus: Optional[str] = field(default=None, repr=False)
    publishedAt: Optional[str] = field(default=None, repr=False)
    updatedAt: Optional[str] = field(default=None, repr=False)


@dataclass
class Comment(BaseResource):
    """
    A class representing comment info.

    Refer: https://developers.google.com/youtube/v3/docs/comments
    """

    snippet: Optional[CommentSnippet] = field(default=None)


@dataclass
class CommentListResponse(BaseApiResponse):
    """
    A class representing the comment's retrieve response info.

    Refer: https://developers.google.com/youtube/v3/docs/comments/list#response_1
    """

    items: Optional[List[Comment]] = field(default=None, repr=False)
