"""
Retrieve some videos info from given channel.

Use pyyoutube.api.get_channel_info to get channel video uploads playlist id.
Then use pyyoutube.api.get_playlist_item to get playlist's videos id.
Last use get_videos_info to get videos data.
"""

import pyyoutube

API_KEY = 'xxx'  # replace this with your api key.


def get_videos(channel_name):
    api = pyyoutube.Api(api_key=API_KEY)
    channel = api.get_channel_info(channel_name=channel_name)

    playlist_id = channel.contentDetails.relatedPlaylists.uploads

    playlist_items, _ = api.get_playlist_item(playlist_id=playlist_id, count=10, limit=6)

    videos = []
    for item in playlist_items:
        video_id = item.contentDetails.videoId
        video_info = api.get_video_info(video_id=video_id)
        videos.append(video_info)
    return videos


def processor():
    channel_name = 'googledevelopers'
    videos = get_videos(channel_name)

    with open('examples/videos.json', 'w+') as f:
        for video in videos:
            f.write(video.as_json_string())
            f.write('\n')


if __name__ == '__main__':
    processor()
