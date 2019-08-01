import unittest
import pyyoutube


class TestApiCall(unittest.TestCase):
    def setUp(self):
        self.api = pyyoutube.Api(
            client_id='xx',
            client_secret='xx',
            api_key='AIzaSyD76JCSGXmMO-_rlAL_yGJuW_ZqsJX33Og'
        )

    def testGetChannel(self):
        res = self.api.get_channel_info(
            channel_name='Nba'
        )
        self.assertEqual(type(res), pyyoutube.PyYouTubeException)

    def testGetVideo(self):
        res = self.api.get_video_info(video_id='Ks-_Mh1QhMc')
        self.assertEqual(type(res), pyyoutube.PyYouTubeException)

    def testGetVideos(self):
        res = self.api.get_videos_info(video_ids=['Ks-_Mh1QhMc', 'c0KYU2j0TM4', 'eIho2S0ZahI'])
        self.assertEqual(type(res), pyyoutube.PyYouTubeException)
