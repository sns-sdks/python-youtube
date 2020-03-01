"""
    These are video abuse report reason related models.
"""

from dataclasses import dataclass, field
from typing import Optional, List

from .base import BaseModel
from .common import BaseResource, BaseApiResponse


@dataclass
class SecondaryReason(BaseModel):
    """
    A class representing the video abuse report reason info

    Refer: https://developers.google.com/youtube/v3/docs/videoAbuseReportReasons#snippet.secondaryReasons
    """

    id: Optional[str] = field(default=None)
    label: Optional[str] = field(default=None, repr=True)


@dataclass
class VideoAbuseReportReasonSnippet(BaseModel):
    """
    A class representing the video abuse report snippet info

    Refer: https://developers.google.com/youtube/v3/docs/videoAbuseReportReasons#snippet
    """

    label: Optional[str] = field(default=None)
    secondaryReasons: Optional[List[SecondaryReason]] = field(default=None, repr=True)


@dataclass
class VideoAbuseReportReason(BaseResource):
    """
    A class representing the video abuse report info

    Refer: https://developers.google.com/youtube/v3/docs/videoAbuseReportReasons
    """

    snippet: Optional[VideoAbuseReportReasonSnippet] = field(default=None)


@dataclass
class VideoAbuseReportReasonListResponse(BaseApiResponse):
    """
    A class representing the I18n language list response info.

    Refer: https://developers.google.com/youtube/v3/docs/videoAbuseReportReasons/list#response_1
    """

    items: Optional[List[VideoAbuseReportReason]] = field(default=None, repr=False)
