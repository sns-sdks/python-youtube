import json
import unittest
import pyyoutube.models as models


class AuthModelTest(unittest.TestCase):
    BASE_PATH = "testdata/modeldata/users/"
    with open(BASE_PATH + "access_token.json", "rb") as f:
        ACCESS_TOKEN_INFO = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "user_profile.json", "rb") as f:
        USER_PROFILE_INFO = json.loads(f.read().decode("utf-8"))

    def testAccessToken(self) -> None:
        m = models.AccessToken.from_dict(self.ACCESS_TOKEN_INFO)

        self.assertEqual(m.access_token, "access_token")

    def testUserProfile(self) -> None:
        m = models.UserProfile.from_dict(self.USER_PROFILE_INFO)

        self.assertEqual(m.id, "12345678910")

        origin_data = json.dumps(self.USER_PROFILE_INFO, sort_keys=True)
        d = m.to_json(sort_keys=True, allow_nan=False)
        self.assertEqual(origin_data, d)
