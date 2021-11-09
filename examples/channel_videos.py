"""
Retrieve some videos info from given channel.

Use pyyoutube.api.get_channel_info to get channel video uploads playlist id.
Then use pyyoutube.api.get_playlist_items to get playlist's videos id.
Last use get_video_by_id to get videos data.
"""

import pyyoutube
import asyncio
import aiohttp


API_KEY = "AIzaSyAm7omealQcFfwnlujF6Xuif8mL7kE7uKg"  # replace this with your api key.


async def get_videos(channel_id):
    async with aiohttp.ClientSession() as session:
        api = pyyoutube.Api(session, api_key=API_KEY)
        channel_res = await api.get_channel_info(channel_id=channel_id)

        playlist_id = channel_res.items[0].contentDetails.relatedPlaylists.uploads

        playlist_item_res = await api.get_playlist_items(
            playlist_id=playlist_id, count=10, limit=6
        )

        videos = []
        for item in playlist_item_res.items:
            video_id = item.contentDetails.videoId
            video_res = await api.get_video_by_id(video_id=video_id)
            videos.extend(video_res.items)
        return videos


async def processor():
    channel_id = "UC_x5XG1OV2P6uZZ5FSM9Ttw"
    videos = await get_videos(channel_id)

    with open("videos.json", "w+") as f:
        for video in videos:
            f.write(video.to_json())
            f.write("\n")


if __name__ == "__main__":
    asyncio.run(processor())
