"""
    These are some mixin for models
"""
import datetime
from typing import Optional

import isodate
from isodate.isoerror import ISO8601Error


class DatetimeTimeMixin:
    @staticmethod
    def string_to_datetime(dt_str: str) -> Optional[datetime.datetime]:
        """
        Convert datetime string to datetime instance.
        original string format is YYYY-MM-DDThh:mm:ss.sZ.
        :return:
        """
        if not dt_str:
            return None
        try:
            r = isodate.parse_datetime(dt_str)
        except ISO8601Error:
            raise
        else:
            return r
