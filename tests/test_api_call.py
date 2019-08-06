import unittest
import pyyoutube

import responses


class TestApiCall(unittest.TestCase):
    BASE_URL = 'https://www.googleapis.com/youtube/v3/'

    def setUp(self):
        self.api = pyyoutube.Api(
            client_id='xx',
            client_secret='xx',
            api_key='xx'
        )

    def testCalcQuota(self):
        self.api.calc_quota(
            resource='videos',
            parts='id,snippet,contentDetails,statistics,status',
        )
        self.assertEqual(9, self.api.used_quota)
        print(self.api.get_quota())
        self.assertEqual(True, '10000' in self.api.get_quota())

    @responses.activate
    def testGetChannel(self):
        with open('testdata/channel_info.json') as f:
            res_data = f.read()
        responses.add(
            responses.GET,
            self.BASE_URL + 'channels',
            body=res_data,
            status=200
        )
        res = self.api.get_channel_info(
            channel_name='Nba'
        )
        self.assertEqual(res.id, 'UCWJ2lWNubArHWmf3FIHbfcQ')

    @responses.activate
    def testGetVideo(self):
        with open('testdata/video_info.json') as f:
            res_data = f.read()
        responses.add(
            responses.GET,
            self.BASE_URL + 'videos',
            body=res_data,
            status=200
        )
        res = self.api.get_video_info(video_id='Ks-_Mh1QhMc')
        self.assertEqual(res.id, 'Ks-_Mh1QhMc')
        self.assertEqual(res.statistics.viewCount, '16729224')

    @responses.activate
    def testGetVideos(self):
        with open('testdata/videos_info.json') as f:
            res_data = f.read()
        responses.add(
            responses.GET,
            self.BASE_URL + 'videos',
            body=res_data,
            status=200
        )
        res = self.api.get_videos_info(video_ids=['c0KYU2j0TM4', 'eIho2S0ZahI'])
        self.assertEqual(len(res), 2)
        self.assertEqual(res[0].id, 'c0KYU2j0TM4')
