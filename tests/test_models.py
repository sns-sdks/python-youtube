import json
import unittest

import pyyoutube


class ModelTest(unittest.TestCase):
    def setUp(self) -> None:
        self.base_path = 'testdata/modeldata/'

    def testAccessToken(self) -> None:
        with open(f'{self.base_path}access_token.json', 'r') as json_file:
            token_info = json.loads(json_file.read())
        m = pyyoutube.AccessToken.new_from_json_dict(token_info)
        self.assertEqual(m.access_token, 'access_token')

    def testUserProfile(self) -> None:
        with open(f'{self.base_path}user_profile.json', 'r') as json_file:
            profile_info = json.loads(json_file.read())
        m = pyyoutube.UserProfile.new_from_json_dict(profile_info)
        self.assertEqual(m.id, '12345678910')

    def testChannel(self) -> None:
        with open(f'{self.base_path}channel_info.json', 'r') as json_file:
            channel_info = json.loads(json_file.read())
        m = pyyoutube.Channel.new_from_json_dict(channel_info)
        self.assertEqual(m.id, 'UCWJ2lWNubArHWmf3FIHbfcQ')
