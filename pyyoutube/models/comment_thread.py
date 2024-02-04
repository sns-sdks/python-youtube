"""
    These are comment threads related models.
"""

from dataclasses import dataclass, field
from typing import Optional, List

from .base import BaseModel
from .common import BaseResource, BaseApiResponse
from .comment import Comment


@dataclass
class CommentThreadSnippet(BaseModel):
    """A class representing comment tread snippet info.

    References: https://developers.google.com/youtube/v3/docs/commentThreads#snippet
    """

    channelId: Optional[str] = field(default=None)
    videoId: Optional[str] = field(default=None)
    topLevelComment: Optional[Comment] = field(default=None, repr=False)
    canReply: Optional[bool] = field(default=None, repr=False)
    totalReplyCount: Optional[int] = field(default=None, repr=False)
    isPublic: Optional[bool] = field(default=None, repr=False)


@dataclass
class CommentThreadReplies(BaseModel):
    """
    A class representing comment tread replies info.

    Refer: https://developers.google.com/youtube/v3/docs/commentThreads#replies
    """

    comments: Optional[List[Comment]] = field(default=None, repr=False)


@dataclass
class CommentThread(BaseResource):
    """
    A class representing comment thread info.

    Refer: https://developers.google.com/youtube/v3/docs/commentThreads
    """

    snippet: Optional[CommentThreadSnippet] = field(default=None, repr=False)
    replies: Optional[CommentThreadReplies] = field(default=None, repr=False)


@dataclass
class CommentThreadListResponse(BaseApiResponse):
    """
    A class representing the comment thread's retrieve response info.

    Refer: https://developers.google.com/youtube/v3/docs/commentThreads/list#response_1
    """

    items: Optional[List[CommentThread]] = field(default=None, repr=False)
