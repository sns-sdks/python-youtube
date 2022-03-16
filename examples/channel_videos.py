"""
Retrieve some videos info from given channel.

Use pyyoutube.api.get_channel_info to get channel video uploads playlist id.
Then use pyyoutube.api.get_playlist_items to get playlist's videos id.
Last use get_video_by_id to get videos data.
"""

import pyyoutube

API_KEY = "xxx"  # replace this with your api key.


def get_videos(channel_id):
    api = pyyoutube.Api(api_key=API_KEY)
    channel_info = api.get_channel_info(channel_id=channel_id)

    playlist_id = channel_info.items[0].contentDetails.relatedPlaylists.uploads

    uploads_playlist_items = api.get_playlist_items(
        playlist_id=playlist_id, count=10, limit=6
    )

    videos = []
    for item in uploads_playlist_items.items:
        video_id = item.contentDetails.videoId
        video = api.get_video_by_id(video_id=video_id)
        videos.extend(video.items)
    return videos


def processor():
    channel_id = "UC_x5XG1OV2P6uZZ5FSM9Ttw"
    videos = get_videos(channel_id)

    with open("videos.json", "w+") as f:
        for video in videos:
            f.write(video.to_json())
            f.write("\n")


if __name__ == "__main__":
    processor()
