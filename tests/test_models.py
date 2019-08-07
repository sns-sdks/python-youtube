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

    def testThumbnail(self) -> None:
        with open(f'{self.base_path}thumbnail_info.json', 'r') as json_file:
            thumbnail_info = json.loads(json_file.read())
        m = pyyoutube.Thumbnail.new_from_json_dict(thumbnail_info)
        self.assertEqual(
            m.url,
            'https://yt3.ggpht.com/a/AGF-l7-BBIcC888A2qYc3rB44rST01IEYDG3uzbU_A=s88-c-k-c0xffffffff-no-rj-mo'
        )

    def testThumbnails(self) -> None:
        with open(f'{self.base_path}thumbnails_info.json', 'r') as json_file:
            thumbnails_info = json.loads(json_file.read())
        m = pyyoutube.Thumbnails.new_from_json_dict(thumbnails_info)
        self.assertEqual(
            m.high.url,
            'https://yt3.ggpht.com/a/AGF-l7-BBIcC888A2qYc3rB44rST01IEYDG3uzbU_A=s800-c-k-c0xffffffff-no-rj-mo'
        )

    def testLocalized(self) -> None:
        with open(f'{self.base_path}localized_info.json', 'r') as json_file:
            localized_info = json.loads(json_file.read())
        m = pyyoutube.Localized.new_from_json_dict(localized_info)
        self.assertEqual(m.title, 'Google')

    def testChannelSnippet(self) -> None:
        with open(f'{self.base_path}channel_snippet.json', 'r') as json_file:
            snippet_info = json.loads(json_file.read())
        m = pyyoutube.ChannelSnippet.new_from_json_dict(snippet_info)
        self.assertEqual(m.title, 'Google')

    def testChannelStatistics(self) -> None:
        with open(f'{self.base_path}channel_statistics.json', 'r') as json_file:
            statistics_info = json.loads(json_file.read())
        m = pyyoutube.ChannelStatistics.new_from_json_dict(statistics_info)
        self.assertEqual(m.viewCount, '2485241484')

    def testRelatedPlaylists(self) -> None:
        with open(f'{self.base_path}related_playlists.json', 'r') as json_file:
            related_playlists_info = json.loads(json_file.read())
        m = pyyoutube.RelatedPlaylists.new_from_json_dict(related_playlists_info)
        self.assertEqual(m.favorites, 'FLK8sQmJBp8GCxrOtXWBpyEA')

    def testChannelContentDetails(self) -> None:
        with open(f'{self.base_path}channel_content_details.json', 'r') as json_file:
            content_details_info = json.loads(json_file.read())
        m = pyyoutube.ChannelContentDetails.new_from_json_dict(content_details_info)
        self.assertEqual(m.relatedPlaylists.favorites, 'FLK8sQmJBp8GCxrOtXWBpyEA')

    def testChannelStatus(self) -> None:
        with open(f'{self.base_path}channel_status.json', 'r') as json_file:
            channel_status_info = json.loads(json_file.read())
        m = pyyoutube.ChannelStatus.new_from_json_dict(channel_status_info)
        self.assertEqual(m.privacyStatus, 'public')

    def testChannel(self) -> None:
        with open(f'{self.base_path}channel_info.json', 'r') as json_file:
            channel_info = json.loads(json_file.read())
        m = pyyoutube.Channel.new_from_json_dict(channel_info)
        self.assertEqual(m.id, 'UCWJ2lWNubArHWmf3FIHbfcQ')

    def testVideoSnippet(self) -> None:
        with open(f'{self.base_path}video_snippet.json', 'r') as json_file:
            video_snippet_info = json.loads(json_file.read())
        m = pyyoutube.VideoSnippet.new_from_json_dict(video_snippet_info)
        self.assertEqual(m.channelId, 'UCK8sQmJBp8GCxrOtXWBpyEA')

    def testVideoStatistics(self) -> None:
        with open(f'{self.base_path}video_statistics.json', 'r') as json_file:
            video_statistics_info = json.loads(json_file.read())
        m = pyyoutube.VideoStatistics.new_from_json_dict(video_statistics_info)
        self.assertEqual(m.viewCount, '7188165')

    def testVideoContentDetails(self) -> None:
        with open(f'{self.base_path}video_content_details.json', 'r') as json_file:
            content_details_info = json.loads(json_file.read())
        m = pyyoutube.VideoContentDetails.new_from_json_dict(content_details_info)
        self.assertEqual(m.duration, 'PT16S')

    def testVideoStatus(self) -> None:
        with open(f'{self.base_path}video_status.json', 'r') as json_file:
            status_info = json.loads(json_file.read())
        m = pyyoutube.VideoStatus.new_from_json_dict(status_info)
        self.assertEqual(m.uploadStatus, 'processed')

    def testVideo(self) -> None:
        with open(f'{self.base_path}video_info.json', 'r') as json_file:
            video_info = json.loads(json_file.read())
        m = pyyoutube.Video.new_from_json_dict(video_info)
        self.assertEqual(m.id, 'lDBbRDfrgnI')
