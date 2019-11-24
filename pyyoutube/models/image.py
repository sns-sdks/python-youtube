"""
    These are image related models
"""
from dataclasses import dataclass, field
from typing import Optional

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
