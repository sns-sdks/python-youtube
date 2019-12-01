"""
Retrieve some videos info from given channel.

Use pyyoutube.api.get_channel_info to get channel video uploads playlist id.
Then use pyyoutube.api.get_playlist_items to get playlist's videos id.
Last use get_video_by_id to get videos data.
"""

import pyyoutube

API_KEY = "xxx"  # replace this with your api key.


def get_videos(channel_name):
    api = pyyoutube.Api(api_key=API_KEY)
    channel_res = api.get_channel_info(channel_name=channel_name)

    playlist_id = channel_res.items[0].contentDetails.relatedPlaylists.uploads

    playlist_item_res = api.get_playlist_items(
        playlist_id=playlist_id, count=10, limit=6
    )

    videos = []
    for item in playlist_item_res.items:
        video_id = item.contentDetails.videoId
        video_res = api.get_video_by_id(video_id=video_id)
        videos = video_res.items
    return videos


def processor():
    channel_name = "googledevelopers"
    videos = get_videos(channel_name)

    with open("videos.json", "w+") as f:
        for video in videos:
            f.write(video.to_json())
            f.write("\n")


if __name__ == "__main__":
    processor()
