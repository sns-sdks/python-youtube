"""
    This provide some common utils methods for YouTube resource.
"""

import isodate
from isodate.isoerror import ISO8601Error

from pyyoutube.error import ErrorMessage, PyYouTubeException


def get_video_duration(duration: str) -> int:
    """
    Parse video ISO 8601 duration to seconds.
    Refer: https://developers.google.com/youtube/v3/docs/videos#contentDetails.duration

    Args:
        duration(str)
            Videos ISO 8601 duration. Like: PT14H23M42S
    Returns:
        integer for seconds.
    """
    try:
        seconds = isodate.parse_duration(duration).total_seconds()
        return int(seconds)
    except ISO8601Error as e:
        raise PyYouTubeException(
            ErrorMessage(
                status_code=10001,
                message=f"Exception in convert video duration: {duration}. errors: {e}",
            )
        )
