import unittest
import pyyoutube


class TestApiCall(unittest.TestCase):
    def setUp(self):
        self.api = pyyoutube.Api(
            client_id='xx',
            client_secret='xx',
            api_key='xx'
        )

    def testGetChannel(self):
        res = self.api.get_channel_info(
            channel_name='Nba'
        )
        self.assertEqual(type(res), pyyoutube.PyYouTubeException)
