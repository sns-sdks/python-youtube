import json
import unittest

import responses
import pyyoutube


class ApiMembersTest(unittest.TestCase):
    BASE_PATH = "testdata/apidata/members/"
    MEMBERS_URL = "https://www.googleapis.com/youtube/v3/members"
    MEMBERSHIP_LEVEL_URL = "https://www.googleapis.com/youtube/v3/membershipsLevels"

    with open(BASE_PATH + "members_data.json", "rb") as f:
        MEMBERS_RES = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "membership_levels.json", "rb") as f:
        MEMBERSHIP_LEVEL_RES = json.loads(f.read().decode("utf-8"))

    def setUp(self) -> None:
        self.api = pyyoutube.Api(access_token="Authorize token")

    def testGetMembers(self) -> None:
        with responses.RequestsMock() as m:
            m.add("GET", self.MEMBERS_URL, json=self.MEMBERS_RES)

            members = self.api.get_members(parts=["id", "snippet"])
            self.assertEqual(members.kind, "youtube#memberListResponse")
            self.assertEqual(len(members.items), 2)

            members_json = self.api.get_members(
                page_token="token",
                count=None,
                has_access_to_level="high",
                filter_by_member_channel_id="id",
                return_json=True,
            )
            self.assertEqual(len(members_json["items"]), 2)

    def testGetMembershipLevels(self) -> None:
        with responses.RequestsMock() as m:
            m.add("GET", self.MEMBERSHIP_LEVEL_URL, json=self.MEMBERSHIP_LEVEL_RES)

            membership_levels = self.api.get_membership_levels(parts=["id", "snippet"])
            self.assertEqual(
                membership_levels.kind, "youtube#membershipsLevelListResponse"
            )
            self.assertEqual(len(membership_levels.items), 2)

            membership_levels_json = self.api.get_membership_levels(return_json=True)
            self.assertEqual(len(membership_levels_json["items"]), 2)
