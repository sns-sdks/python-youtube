"""
    These are some mixin for models
"""
import datetime
from typing import Optional

import isodate
from isodate.isoerror import ISO8601Error

from pyyoutube.error import ErrorCode, ErrorMessage, PyYouTubeException


class DatetimeTimeMixin:
    @staticmethod
    def string_to_datetime(dt_str: Optional[str]) -> Optional[datetime.datetime]:
        """
        Convert datetime string to datetime instance.
        original string format is YYYY-MM-DDThh:mm:ss.sZ.
        :return:
        """
        if not dt_str:
            return None
        try:
            r = isodate.parse_datetime(dt_str)
        except ISO8601Error as e:
            raise PyYouTubeException(
                ErrorMessage(status_code=ErrorCode.INVALID_PARAMS, message=e.args[0])
            )
        else:
            return r
