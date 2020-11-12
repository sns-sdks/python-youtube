"""
    These are member related models.
"""

from dataclasses import dataclass, field
from typing import List, Optional

from .base import BaseModel
from .common import BaseApiResponse
from .mixins import DatetimeTimeMixin


@dataclass
class MemberSnippetMemberDetails(BaseModel):
    """
    A class representing the member snippet member detail.

    Refer: https://developers.google.com/youtube/v3/docs/members#snippet.memberDetails
    """

    channelId: Optional[str] = field(default=None)
    channelUrl: Optional[str] = field(default=None, repr=False)
    displayName: Optional[str] = field(default=None, repr=False)
    profileImageUrl: Optional[str] = field(default=None, repr=False)


@dataclass
class MemberSnippetMembershipsDuration(BaseModel, DatetimeTimeMixin):
    memberSince: Optional[str] = field(default=None)
    memberTotalDurationMonths: Optional[int] = field(default=None, repr=False)


@dataclass
class MemberSnippetMembershipsDurationAtLevel(BaseModel):
    level: Optional[str] = field(default=None)
    memberSince: Optional[str] = field(default=None, repr=False)
    memberTotalDurationMonths: Optional[int] = field(default=None, repr=False)


@dataclass
class MemberSnippetMembershipsDetails(BaseModel):
    """
    A class representing the member snippet membership detail.

    Refer: https://developers.google.com/youtube/v3/docs/members#snippet.membershipsDetails
    """

    highestAccessibleLevel: Optional[str] = field(default=None)
    highestAccessibleLevelDisplayName: Optional[str] = field(default=None)
    accessibleLevels: Optional[List[str]] = field(default=None, repr=False)
    membershipsDuration: Optional[MemberSnippetMembershipsDuration] = field(
        default=None, repr=False
    )
    membershipsDurationAtLevel: Optional[
        List[MemberSnippetMembershipsDurationAtLevel]
    ] = field(default=None, repr=False)


@dataclass
class MemberSnippet(BaseModel):
    """
    A class representing the member snippet info.

    Refer: https://developers.google.com/youtube/v3/docs/members#snippet
    """

    creatorChannelId: Optional[str] = field(default=None)
    memberDetails: Optional[MemberSnippetMemberDetails] = field(
        default=None, repr=False
    )
    membershipsDetails: Optional[MemberSnippetMembershipsDetails] = field(
        default=None, repr=False
    )


@dataclass
class Member(BaseModel):
    """
    A class representing the member info.

    Refer: https://developers.google.com/youtube/v3/docs/members
    """

    kind: Optional[str] = field(default=None)
    etag: Optional[str] = field(default=None, repr=False)
    snippet: Optional[MemberSnippet] = field(default=None, repr=False)


@dataclass
class MemberListResponse(BaseApiResponse):
    """
    A class representing the member's retrieve response info.

    Refer: https://developers.google.com/youtube/v3/docs/members/list#response
    """

    items: Optional[List[Member]] = field(default=None, repr=False)
