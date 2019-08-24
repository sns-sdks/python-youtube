import json
import unittest

import pyyoutube


class ModelTest(unittest.TestCase):
    def setUp(self) -> None:
        self.base_path = 'testdata/modeldata/'

    def testAccessToken(self) -> None:
        with open(f'{self.base_path}access_token.json', 'rb') as json_file:
            token_info = json.loads(json_file.read())
        m = pyyoutube.AccessToken.new_from_json_dict(token_info)
        try:
            m.__repr__()
        except Exception as e:
            self.fail(e)

        self.assertEqual(m.access_token, 'access_token')

    def testUserProfile(self) -> None:
        with open(f'{self.base_path}user_profile.json', 'rb') as json_file:
            profile_info = json.loads(json_file.read())
        m = pyyoutube.UserProfile.new_from_json_dict(profile_info)
        try:
            m.__repr__()
        except Exception as e:
            self.fail(e)

        self.assertEqual(m.id, '12345678910')

    def testThumbnail(self) -> None:
        with open(f'{self.base_path}thumbnail_info.json', 'rb') as json_file:
            thumbnail_info = json.loads(json_file.read())
        m = pyyoutube.Thumbnail.new_from_json_dict(thumbnail_info)
        try:
            m.__repr__()
        except Exception as e:
            self.fail(e)

        self.assertEqual(
            m.url,
            'https://yt3.ggpht.com/a/AGF-l7-BBIcC888A2qYc3rB44rST01IEYDG3uzbU_A=s88-c-k-c0xffffffff-no-rj-mo'
        )

    def testThumbnails(self) -> None:
        with open(f'{self.base_path}thumbnails_info.json', 'rb') as json_file:
            thumbnails_info = json.loads(json_file.read())
        m = pyyoutube.Thumbnails.new_from_json_dict(thumbnails_info)
        try:
            m.__repr__()
        except Exception as e:
            self.fail(e)
        self.assertEqual(
            m.high.url,
            'https://yt3.ggpht.com/a/AGF-l7-BBIcC888A2qYc3rB44rST01IEYDG3uzbU_A=s800-c-k-c0xffffffff-no-rj-mo'
        )

    def testChannelBrandingSetting(self) -> None:
        with open(f'{self.base_path}channel_branding_settings.json', 'rb') as json_file:
            channel_branding_settings = json.loads(json_file.read())
        m = pyyoutube.ChannelBrandingSetting.new_from_json_dict(channel_branding_settings)
        try:
            m.__repr__()
            m.channel.__repr__()
            m.image.__repr__()
            m.hints[0].__repr__()
        except Exception as e:
            self.fail(e)

        self.assertEqual(m.channel.title, 'Google Developers')
        self.assertEqual(
            m.image.bannerImageUrl,
            ('https://yt3.ggpht.com/vpeUmkxH-uuOYgdvyCXg5Bz4Rn5z2Yxj_'
             'efZ2uN62WZeQFdro2PfumdcvvLJwn9G4mRFyriF7Vk=w1060-fcrop64=1,'
             '00005a57ffffa5a8-k-c0xffffffff-no-nd-rj'),
        )
        self.assertEqual(len(m.hints), 2)
        self.assertEqual(m.hints[0].property, 'channel.banner.mobile.medium.image.url')

    def testChannelContentDetails(self) -> None:
        with open(f'{self.base_path}channel_content_details.json', 'rb') as json_file:
            content_details_info = json.loads(json_file.read())
        m = pyyoutube.ChannelContentDetails.new_from_json_dict(content_details_info)
        try:
            m.__repr__()
            m.relatedPlaylists.__repr__()
        except Exception as e:
            self.fail(e)
        self.assertEqual(m.relatedPlaylists.uploads, 'UU_x5XG1OV2P6uZZ5FSM9Ttw')

    def testChannelTopicDetails(self) -> None:
        with open(f'{self.base_path}channel_topic_details.json', 'rb') as json_file:
            channel_topic_details = json.loads(json_file.read())
        m = pyyoutube.ChannelTopicDetails.new_from_json_dict(channel_topic_details)
        try:
            m.__repr__()
            m.topicIds[0].__repr__()
        except Exception as e:
            self.fail(e)
        self.assertEqual(m.topicIds[0].id, '/m/019_rr')
        self.assertEqual(m.topicIds[0].description, 'Lifestyle (parent topic)')
        self.assertEqual(len(m.topicCategories), 3)

    def testChannelSnippet(self) -> None:
        with open(f'{self.base_path}channel_snippet.json', 'rb') as json_file:
            snippet_info = json.loads(json_file.read())
        m = pyyoutube.ChannelSnippet.new_from_json_dict(snippet_info)
        try:
            m.__repr__()
            m.localized.__repr__()
        except Exception as e:
            self.fail(e)

        self.assertEqual(m.title, 'Google Developers')
        self.assertEqual(m.localized.title, 'Google Developers')
        self.assertEqual(
            m.thumbnails.default.url,
            'https://yt3.ggpht.com/a/AGF-l78iFtAxyRZcUBzG91kbKMES19z-zGW5KT20_g=s88-c-k-c0xffffffff-no-rj-mo'
        )

    def testChannelStatistics(self) -> None:
        with open(f'{self.base_path}channel_statistics.json', 'rb') as json_file:
            statistics_info = json.loads(json_file.read())
        m = pyyoutube.ChannelStatistics.new_from_json_dict(statistics_info)
        try:
            m.__repr__()
        except Exception as e:
            self.fail(e)

        self.assertEqual(m.viewCount, '160361638')

    def testChannelStatus(self) -> None:
        with open(f'{self.base_path}channel_status.json', 'rb') as json_file:
            channel_status_info = json.loads(json_file.read())
        m = pyyoutube.ChannelStatus.new_from_json_dict(channel_status_info)
        try:
            m.__repr__()
        except Exception as e:
            self.fail(e)

        self.assertEqual(m.privacyStatus, 'public')

    def testChannel(self) -> None:
        with open(f'{self.base_path}channel_info.json', 'rb') as json_file:
            channel_info = json.loads(json_file.read())
        m = pyyoutube.Channel.new_from_json_dict(channel_info)
        try:
            m.__repr__()
        except Exception as e:
            self.fail(e)

        origin_json_data = json.dumps(channel_info, sort_keys=True)
        self.assertEqual(origin_json_data, m.as_json_string())
        self.assertEqual(channel_info, m.as_dict())
        self.assertEqual(m.id, 'UC_x5XG1OV2P6uZZ5FSM9Ttw')

    def testVideoContentDetails(self) -> None:
        with open(f'{self.base_path}video_content_details.json', 'rb') as json_file:
            content_details_info = json.loads(json_file.read())
        m = pyyoutube.VideoContentDetails.new_from_json_dict(content_details_info)
        try:
            m.__repr__()
        except Exception as e:
            self.fail(e)

        self.assertEqual(m.duration, 'PT21M7S')

    def testVideoTopicDetails(self) -> None:
        with open(f'{self.base_path}video_topic_details.json', 'rb') as json_file:
            video_topic_details = json.loads(json_file.read())
        m = pyyoutube.VideoTopicDetails.new_from_json_dict(video_topic_details)
        try:
            m.__repr__()
            m.topicIds[0].__repr__()
            m.relevantTopicIds[0].__repr__()
        except Exception as e:
            self.fail(e)
        self.assertEqual(m.topicIds[0].id, '/m/02jjt')
        self.assertEqual(m.topicIds[0].description, 'Entertainment (parent topic)')
        self.assertEqual(len(m.topicCategories), 1)

    def testVideoSnippet(self) -> None:
        with open(f'{self.base_path}video_snippet.json', 'rb') as json_file:
            video_snippet_info = json.loads(json_file.read())
        m = pyyoutube.VideoSnippet.new_from_json_dict(video_snippet_info)
        try:
            m.__repr__()
        except Exception as e:
            self.fail(e)

        self.assertEqual(m.channelId, 'UC_x5XG1OV2P6uZZ5FSM9Ttw')

    def testVideoStatistics(self) -> None:
        with open(f'{self.base_path}video_statistics.json', 'rb') as json_file:
            video_statistics_info = json.loads(json_file.read())
        m = pyyoutube.VideoStatistics.new_from_json_dict(video_statistics_info)
        try:
            m.__repr__()
        except Exception as e:
            self.fail(e)

        self.assertEqual(m.viewCount, '8087')

    def testVideoStatus(self) -> None:
        with open(f'{self.base_path}video_status.json', 'rb') as json_file:
            status_info = json.loads(json_file.read())
        m = pyyoutube.VideoStatus.new_from_json_dict(status_info)
        try:
            m.__repr__()
        except Exception as e:
            self.fail(e)

        self.assertEqual(m.uploadStatus, 'processed')

    def testVideo(self) -> None:
        with open(f'{self.base_path}video_info.json', 'rb') as json_file:
            video_info = json.loads(json_file.read())
        m = pyyoutube.Video.new_from_json_dict(video_info)
        try:
            m.__repr__()
        except Exception as e:
            self.fail(e)

        self.assertEqual(m.id, 'D-lhorsDlUQ')
        self.assertEqual(video_info['id'], m.as_dict()['id'])

    def testPlayList(self) -> None:
        with open(f'{self.base_path}playlist_info.json', 'rb') as json_file:
            playlist_info = json.loads(json_file.read())
        m = pyyoutube.PlayList.new_from_json_dict(playlist_info)
        try:
            m.__repr__()
        except Exception as e:
            self.fail(e)

        self.assertEqual(m.id, 'PLOU2XLYxmsIJpufeMHncnQvFOe0K3MhVp')

    def testPlayListSnippet(self) -> None:
        with open(f'{self.base_path}playlist_snippet.json', 'rb') as json_file:
            playlist_snippet = json.loads(json_file.read())
        m = pyyoutube.PlayListSnippet.new_from_json_dict(playlist_snippet)
        try:
            m.__repr__()
        except Exception as e:
            self.fail(e)

        self.assertEqual(m.title, 'Assistant on Air')

    def testPlayListStatus(self) -> None:
        with open(f'{self.base_path}playlist_status.json', 'rb') as json_file:
            playlist_status = json.loads(json_file.read())
        m = pyyoutube.PlayListStatus.new_from_json_dict(playlist_status)
        try:
            m.__repr__()
        except Exception as e:
            self.fail(e)

        self.assertEqual(m.privacyStatus, 'public')

    def testPlayListContentDetails(self) -> None:
        with open(f'{self.base_path}playlist_content_details.json', 'rb') as json_file:
            playlist_content_details = json.loads(json_file.read())
        m = pyyoutube.PlayListContentDetails.new_from_json_dict(playlist_content_details)
        try:
            m.__repr__()
        except Exception as e:
            self.fail(e)

        self.assertEqual(m.itemCount, 4)

    def testPlaylistItem(self) -> None:
        with open(f'{self.base_path}playlist_item_info.json', 'rb') as json_file:
            playlist_item_info = json.loads(json_file.read())
        m = pyyoutube.PlaylistItem.new_from_json_dict(playlist_item_info)
        try:
            m.__repr__()
        except Exception as e:
            self.fail(e)

        origin_json_data = json.dumps(playlist_item_info, sort_keys=True)
        self.assertEqual(origin_json_data, m.as_json_string())
        self.assertEqual(playlist_item_info, m.as_dict())

        self.assertEqual(m.id, 'UExPVTJYTFl4bXNJSnB1ZmVNSG5jblF2Rk9lMEszTWhWcC41NkI0NEY2RDEwNTU3Q0M2')

    def testResourceId(self) -> None:
        with open(f'{self.base_path}resource_id_info.json', 'rb') as json_file:
            resource_id_info = json.loads(json_file.read())
        m = pyyoutube.ResourceId.new_from_json_dict(resource_id_info)
        try:
            m.__repr__()
        except Exception as e:
            self.fail(e)

        self.assertEqual(m.videoId, 'D-lhorsDlUQ')

    def testPlaylistItemSnippet(self) -> None:
        with open(f'{self.base_path}playlist_item_snippet.json', 'rb') as json_file:
            playlist_item_snippet = json.loads(json_file.read())
        m = pyyoutube.PlaylistItemSnippet.new_from_json_dict(playlist_item_snippet)
        try:
            m.__repr__()
        except Exception as e:
            self.fail(e)

        self.assertEqual(m.title, 'What are Actions on Google (Assistant on Air)')

    def testPlaylistItemContentDetails(self) -> None:
        with open(f'{self.base_path}playlist_item_content_details.json', 'rb') as json_file:
            playlist_item_content_details = json.loads(json_file.read())
        m = pyyoutube.PlaylistItemContentDetails.new_from_json_dict(playlist_item_content_details)
        try:
            m.__repr__()
        except Exception as e:
            self.fail(e)

        self.assertEqual(m.videoId, 'D-lhorsDlUQ')

    def testPlaylistItemStatus(self) -> None:
        with open(f'{self.base_path}playlist_item_status.json', 'rb') as json_file:
            playlist_item_status = json.loads(json_file.read())
        m = pyyoutube.PlaylistItemStatus.new_from_json_dict(playlist_item_status)
        try:
            m.__repr__()
        except Exception as e:
            self.fail(e)

        self.assertEqual(m.privacyStatus, 'public')

    def testCommentSnippet(self) -> None:
        with open(f'{self.base_path}comment_snippet.json', 'rb') as json_file:
            comment_snippet = json.loads(json_file.read())
        m = pyyoutube.CommentSnippet.new_from_json_dict(comment_snippet)
        try:
            m.__repr__()
        except Exception as e:
            self.fail(e)

        self.assertEqual(m.videoId, 'wtLJPvx7-ys')

    def testComment(self) -> None:
        with open(f'{self.base_path}comment_info.json', 'rb') as json_file:
            comment = json.loads(json_file.read())
        m = pyyoutube.Comment.new_from_json_dict(comment)
        try:
            m.__repr__()
        except Exception as e:
            self.fail(e)

        self.assertEqual(m.id, 'UgwxApqcfzZzF_C5Zqx4AaABAg')

    def testCommentTreadSnippet(self) -> None:
        with open(f'{self.base_path}comment_tread_snippet.json', 'rb') as json_file:
            comment_tread_snippet = json.loads(json_file.read())
        m = pyyoutube.CommentTreadSnippet.new_from_json_dict(comment_tread_snippet)
        try:
            m.__repr__()
        except Exception as e:
            self.fail(e)

        self.assertEqual(m.videoId, 'D-lhorsDlUQ')

    def testCommentTreadReplies(self) -> None:
        with open(f'{self.base_path}comment_tread_replies.json', 'rb') as json_file:
            comment_tread_replies = json.loads(json_file.read())
        m = pyyoutube.CommentTreadReplies.new_from_json_dict(comment_tread_replies)
        try:
            m.__repr__()
        except Exception as e:
            self.fail(e)

        self.assertEqual(len(m.comments), 1)
        self.assertEqual(comment_tread_replies, m.as_dict())

    def testCommentTread(self) -> None:
        with open(f'{self.base_path}comment_tread_info.json', 'rb') as json_file:
            comment_tread_info = json.loads(json_file.read())
        m = pyyoutube.CommentTread.new_from_json_dict(comment_tread_info)
        try:
            m.__repr__()
        except Exception as e:
            self.fail(e)

        self.assertEqual(m.id, 'UgydxWWoeA7F1OdqypJ4AaABAg')
