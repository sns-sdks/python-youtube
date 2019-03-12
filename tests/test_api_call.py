import unittest
import pyyoutube


class TestApiCall(unittest.TestCase):
    def setUp(self):
        self.api = pyyoutube.Api(
            # client_id='xx',
            # client_secret='xx',
            # api_key='xx'
            client_id='250705703568-r4f3cj6s6uo9bleja0vp4s3d1e35h8pj.apps.googleusercontent.com',
            client_secret='uJWl0FbKmCXd5fKM8SE4kKKj', api_key='AIzaSyAOQfAh5XtLldjXeOgzB2l_2f7eIHTjwcY'
        )

    def testGetChannel(self):
        res = self.api.get_channel_info(
            channel_name='Nba'
        )
        self.assertEqual(type(res), pyyoutube.PyYouTubeException)

    def testGetVideo(self):
        res = self.api.get_video_info(video_id='Ks-_Mh1QhMc')
        self.assertEqual(type(res), pyyoutube.PyYouTubeException)
