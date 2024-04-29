"""
Retrieve channel's videos by search api.

Note Quota impact: A call to this method has a quota cost of 100 units.
"""

import pyyoutube

API_KEY = "xxx"  # replace this with your api key.


def get_all_videos_id_by_channel(channel_id, limit=50, count=50):
    api = pyyoutube.Api(api_key=API_KEY)

    videos = []
    next_page = None

    while True:
        res = api.search(
            channel_id=channel_id,
            limit=limit,
            count=count,
            page_token=next_page,
        )

        next_page = res.nextPageToken

        for item in res.items:
            if item.id.videoId:
                videos.append(item.id.videoId)

        if not next_page:
            break

    return videos
