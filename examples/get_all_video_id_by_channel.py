"""
Retrieve some videos info from given channel.

Use pyyoutube.api.get_channel_info to get channel video uploads playlist id.
Then use pyyoutube.api.get_playlist_items to get playlist's videos id.
Last use get_video_by_id to get videos data.
"""

import pyyoutube

API_KEY = "xxx"  # replace this with your api key.

def get_all_videos_id_by_channel(channel_id, limit=50, count=50):
    api = pyyoutube.Api(api_key=API_KEY)
    res = api.search(channel_id=channel_id, limit=limit, count=count)
    nextPage = res.nextPageToken
    videos_id = []
    
    while nextPage:
        nextPage = res.nextPageToken
        for item in res.items:
            if item.id.videoId:
                videos_id.append(item.id.videoId)
        
        res = api.search(channel_id=channel_id, limit=limit, count=count, page_token=res.nextPageToken)
    
    return videos_id

