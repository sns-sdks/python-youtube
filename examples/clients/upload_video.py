"""
    This example demonstrates how to upload a video.
"""

import pyyoutube.models as mds
from pyyoutube import Client
from pyyoutube.media import Media

# Access token with scope:
# https://www.googleapis.com/auth/youtube.upload
# https://www.googleapis.com/auth/youtube
# https://www.googleapis.com/auth/youtube.force-ssl
ACCESS_TOKEN = "xxx"


def upload_video():
    cli = Client(access_token=ACCESS_TOKEN)

    body = mds.Video(
        snippet=mds.VideoSnippet(title="video title", description="video description")
    )

    media = Media(filename="target_video.mp4")

    upload = cli.videos.insert(
        body=body, media=media, parts=["snippet"], notify_subscribers=True
    )

    response = None
    while response is None:
        print(f"Uploading video...")
        status, response = upload.next_chunk()
        if status is not None:
            print(f"Uploading video progress: {status.progress()}...")

    # Use video class to representing the video resource.
    video = mds.Video.from_dict(response)
    print(f"Video id {video.id} was successfully uploaded.")


if __name__ == "__main__":
    upload_video()
