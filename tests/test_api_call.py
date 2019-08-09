import unittest
import pyyoutube

import responses


class TestApiCall(unittest.TestCase):
    BASE_URL = 'https://www.googleapis.com/youtube/v3/'

    def setUp(self):
        self.base_path = '../testdata/'
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
        self.assertEqual(True, '10000' in self.api.get_quota())

    @responses.activate
    def testGetChannel(self):
        with open(f'{self.base_path}channel_info.json') as f:
            res_data = f.read()
        responses.add(
            responses.GET,
            self.BASE_URL + 'channels',
            body=res_data,
            status=200
        )
        res = self.api.get_channel_info(
            channel_name='GoogleDevelopers'
        )
        self.assertEqual(res.id, 'UC_x5XG1OV2P6uZZ5FSM9Ttw')

    @responses.activate
    def testGetVideo(self):
        with open(f'{self.base_path}video_info.json') as f:
            res_data = f.read()
        responses.add(
            responses.GET,
            self.BASE_URL + 'videos',
            body=res_data,
            status=200
        )
        res = self.api.get_video_info(video_id='Ks-_Mh1QhMc')
        self.assertEqual(res.id, 'D-lhorsDlUQ')
        self.assertEqual(res.statistics.viewCount, '7920')

    @responses.activate
    def testGetVideos(self):
        with open(f'{self.base_path}videos_info.json') as f:
            res_data = f.read()
        responses.add(
            responses.GET,
            self.BASE_URL + 'videos',
            body=res_data,
            status=200
        )
        res = self.api.get_videos_info(video_ids=['ffdXLm8EaYg', 'plhVMWR33go'])
        self.assertEqual(len(res), 2)
        self.assertEqual(res[0].id, 'ffdXLm8EaYg')
