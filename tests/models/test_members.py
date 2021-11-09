import json
import unittest

import pyyoutube.models as models


class MemberModelTest(unittest.IsolatedAsyncioTestCase):
    BASE_PATH = "testdata/modeldata/members/"

    with open(BASE_PATH + "member_info.json", "rb") as f:
        MEMBER_INFO = json.loads(f.read().decode("utf-8"))

    async def testMember(self) -> None:
        m = models.Member.from_dict(self.MEMBER_INFO)

        self.assertEqual(m.kind, "youtube#member")
        self.assertEqual(m.snippet.memberDetails.channelId, "UCa-vrCLQHviTOVnEKDOdetQ")
        self.assertEqual(m.snippet.membershipsDetails.highestAccessibleLevel, "string")


class MembershipLevelModelTest(unittest.IsolatedAsyncioTestCase):
    BASE_PATH = "testdata/modeldata/members/"

    with open(BASE_PATH + "membership_level.json", "rb") as f:
        MEMBERSHIP_LEVEL_INFO = json.loads(f.read().decode("utf-8"))

    async def testMembershipLevel(self) -> None:
        m = models.MembershipsLevel.from_dict(self.MEMBERSHIP_LEVEL_INFO)

        self.assertEqual(m.kind, "youtube#membershipsLevel")
        self.assertEqual(m.snippet.levelDetails.displayName, "high")
