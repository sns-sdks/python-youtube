import unittest
import pyyoutube

import responses


class TestApiCall(unittest.TestCase):
    BASE_URL = 'https://www.googleapis.com/youtube/v3/'

    def setUp(self):
        self.base_path = 'testdata/'
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
    def testGetPlaylist(self):
        with open(f'{self.base_path}playlists_info.json') as f:
            res_data = f.read()
        responses.add(
            responses.GET,
            self.BASE_URL + 'playlists',
            body=res_data,
            status=200
        )

        playlists, summary = self.api.get_playlist(
            channel_id='UC_x5XG1OV2P6uZZ5FSM9Ttw',
            limit=5,
        )
        self.assertEqual(len(playlists), 5)
        self.assertEqual(playlists[0].id, 'PLOU2XLYxmsIJpufeMHncnQvFOe0K3MhVp')
        self.assertEqual(summary['totalResults'], 416)

    @responses.activate
    def testGetPlaylistItems(self):
        with open(f'{self.base_path}playlist_items_info.json') as f:
            res_data = f.read()
        responses.add(
            responses.GET,
            self.BASE_URL + 'playlistItems',
            body=res_data,
            status=200
        )

        playlist_items, summary = self.api.get_playlist_item(
            playlist_id='PLOU2XLYxmsIJJVnHWmd1qfr0Caq4VZCu4',
            limit=5,
        )
        self.assertEqual(len(playlist_items), 5)
        self.assertEqual(playlist_items[0].id, 'UExPVTJYTFl4bXNJSkpWbkhXbWQxcWZyMENhcTRWWkN1NC4zRjM0MkVCRTg0MkYyQTM0')
        self.assertEqual(summary['totalResults'], 23)

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

    @responses.activate
    def testGetCommentThreads(self) -> None:
        with open(f'{self.base_path}comment_threads_by_all_to_channel_id.json') as f:
            res_data_by_all = f.read()
        with open(f'{self.base_path}comment_threads_by_video_id.json') as f:
            res_data_by_video = f.read()
        responses.add(
            responses.GET,
            self.BASE_URL + 'commentThreads',
            body=res_data_by_all, status=200,
        )
        responses.add(
            responses.GET,
            self.BASE_URL + 'commentThreads',
            body=res_data_by_video, status=200,
        )
        with self.assertRaises(pyyoutube.PyYouTubeException):
            self.api.get_comment_threads()
        with self.assertRaises(pyyoutube.PyYouTubeException):
            self.api.get_comment_threads(channel_id='channel id', order='rev')

        comment_threads = self.api.get_comment_threads(
            all_to_channel_id='UC_x5XG1OV2P6uZZ5FSM9Ttw',
            count=4,
        )
        self.assertEqual(len(comment_threads), 4)
        self.assertEqual(comment_threads[0].id, 'UgzhytyP79_PwaDd4UB4AaABAg')

        comment_threads_by_video = self.api.get_comment_threads(video_id='D-lhorsDlUQ', return_json=True)
        self.assertEqual(len(comment_threads_by_video), 5)
        self.assertEqual(comment_threads_by_video[0]['id'], 'UgydxWWoeA7F1OdqypJ4AaABAg')

    @responses.activate
    def testGetCommentThreadInfo(self) -> None:
        with open(f'{self.base_path}comment_threads_by_id.json') as f:
            res_data = f.read()

        responses.add(
            responses.GET,
            self.BASE_URL + 'commentThreads',
            body=res_data, status=200
        )

        with self.assertRaises(pyyoutube.PyYouTubeException):
            self.api.get_comment_thread_info()

        comment_threads = self.api.get_comment_thread_info('Ugz097FRhsQy5CVhAjp4AaABAg,UgzhytyP79_PwaDd4UB4AaABAg')
        self.assertEqual(len(comment_threads), 2)

        comment_threads = self.api.get_comment_thread_info(
            'Ugz097FRhsQy5CVhAjp4AaABAg,UgzhytyP79_PwaDd4UB4AaABAg',
            return_json=True
        )
        self.assertEqual(comment_threads[0]['id'], 'Ugz097FRhsQy5CVhAjp4AaABAg')

    @responses.activate
    def testGetCommentsByParent(self) -> None:
        with open(f'{self.base_path}comments_by_parent_id.json') as f:
            res_data_by_parent = f.read()
        responses.add(
            responses.GET,
            self.BASE_URL + 'comments',
            body=res_data_by_parent, status=200
        )

        with self.assertRaises(pyyoutube.PyYouTubeException):
            self.api.get_comments_by_parent()

        comments = self.api.get_comments_by_parent(parent_id='UgwYjZXfNCUTKPq9CZp4AaABAg', count=1)
        self.assertEqual(len(comments), 1)

        comments = self.api.get_comments_by_parent(parent_id='UgwYjZXfNCUTKPq9CZp4AaABAg', return_json=True)
        self.assertEqual(comments[0]['id'], 'UgwYjZXfNCUTKPq9CZp4AaABAg.8yxhlQJogG18yz_cXK9Kcj')

    @responses.activate
    def testGetCommentInfo(self) -> None:
        with open(f'{self.base_path}comments_by_id.json') as f:
            res_data_by_id = f.read()
        responses.add(
            responses.GET,
            self.BASE_URL + 'comments',
            body=res_data_by_id, status=200
        )
        with self.assertRaises(pyyoutube.PyYouTubeException):
            self.api.get_comment_info()

        comments = self.api.get_comment_info(comment_id='UgxKREWxIgDrw8w2e_Z4AaABAg,UgyrVQaFfEdvaSzstj14AaABAg')
        self.assertEqual(len(comments), 2)
        comments = self.api.get_comment_info(
            comment_id='UgxKREWxIgDrw8w2e_Z4AaABAg,UgyrVQaFfEdvaSzstj14AaABAg',
            return_json=True
        )
        self.assertEqual(comments[0]['id'], 'UgxKREWxIgDrw8w2e_Z4AaABAg')
