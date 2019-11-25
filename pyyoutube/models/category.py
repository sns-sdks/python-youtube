"""
    These are category related models.
    Include VideoCategory and GuideCategory.
"""
from dataclasses import dataclass, field
from typing import Optional

from .base import BaseModel
from .comment import BaseResource


@dataclass
class CategorySnippet(BaseModel):
    """
    This is base category snippet for video and guide.
    """

    channelId: Optional[str] = field(default=None)
    title: Optional[str] = field(default=None)


@dataclass
class VideoCategorySnippet(CategorySnippet):
    """
    A class representing video category snippet info.

    Refer: https://developers.google.com/youtube/v3/docs/videoCategories#snippet
    """

    assignable: Optional[bool] = field(default=None, repr=False)


@dataclass
class VideoCategory(BaseResource):
    """
    A class representing video category info.

    Refer: https://developers.google.com/youtube/v3/docs/videoCategories
    """

    snippet: Optional[VideoCategorySnippet] = field(default=None, repr=False)


@dataclass
class GuideCategorySnippet(CategorySnippet):
    """
    A class representing guide category snippet info.

    Refer: https://developers.google.com/youtube/v3/docs/guideCategories#snippet
    """

    ...


@dataclass
class GuideCategory(BaseResource):
    """
    A class representing guide category snippet.

    Refer: https://developers.google.com/youtube/v3/docs/guideCategories
    """

    snippet: Optional[GuideCategorySnippet] = field(default=None, repr=False)
