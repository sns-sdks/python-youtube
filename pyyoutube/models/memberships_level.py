"""
    These are membership level related models.
"""

from dataclasses import dataclass, field
from typing import List, Optional

from .base import BaseModel
from .common import BaseResource, BaseApiResponse


@dataclass
class MembershipLevelSnippetLevelDetails(BaseModel):
    displayName: Optional[str] = field(default=None)


@dataclass
class MembershipsLevelSnippet(BaseModel):
    """
    A class representing the membership level snippet.

    Refer: https://developers.google.com/youtube/v3/docs/membershipsLevels#snippet
    """

    creatorChannelId: Optional[str] = field(default=None)
    levelDetails: Optional[MembershipLevelSnippetLevelDetails] = field(
        default=None, repr=False
    )


@dataclass
class MembershipsLevel(BaseResource):
    """
    A class representing the membership level.

    Refer: https://developers.google.com/youtube/v3/docs/membershipsLevels
    """

    snippet: Optional[MembershipsLevelSnippet] = field(default=None, repr=False)


@dataclass
class MembershipsLevelListResponse(BaseApiResponse):
    """
    A class representing the memberships level's retrieve response info.

    Refer: https://developers.google.com/youtube/v3/docs/membershipsLevels/list#response
    """

    items: Optional[List[MembershipsLevel]] = field(default=None, repr=False)
