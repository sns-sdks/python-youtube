"""
    function's params checker.
"""
import logging

from typing import Optional, Union

from pyyoutube.error import ErrorCode, ErrorMessage, PyYouTubeException
from pyyoutube.utils.constants import RESOURCE_PARTS_MAPPING

logger = logging.getLogger(__name__)


def enf_comma_separated(
    field: str,
    value: Optional[Union[str, list, tuple, set]],
):
    """
    Check to see if field's value type belong to correct type.
    If it is, return api need value, otherwise, raise a PyYouTubeException.

    Args:
        field (str):
            Name of the field you want to do check.
        value (str, list, tuple, set, Optional)
            Value for the field.

    Returns:
        Api needed string
    """
    if value is None:
        return None
    try:
        if isinstance(value, str):
            return value
        elif isinstance(value, (list, tuple, set)):
            if isinstance(value, set):
                logging.warning(f"Note: The order of the set is unreliable.")
            return ",".join(value)
        else:
            raise PyYouTubeException(
                ErrorMessage(
                    status_code=ErrorCode.INVALID_PARAMS,
                    message=f"Parameter ({field}) must be single str,comma-separated str,list,tuple or set",
                )
            )
    except (TypeError, ValueError):
        raise PyYouTubeException(
            ErrorMessage(
                status_code=ErrorCode.INVALID_PARAMS,
                message=f"Parameter ({field}) must be single str,comma-separated str,list,tuple or set",
            )
        )


def enf_parts(resource: str, value: Optional[Union[str, list, tuple, set]], check=True):
    """
    Check to see if value type belong to correct type, and if resource support the given part.
    If it is, return api need value, otherwise, raise a PyYouTubeException.

    Args:
        resource (str):
            Name of the resource you want to retrieve.
        value (str, list, tuple, set, Optional):
            Value for the part.
        check (bool, optional):
            Whether check the resource properties.

    Returns:
        Api needed part string
    """
    if value is None:
        parts = RESOURCE_PARTS_MAPPING[resource]
    elif isinstance(value, str):
        parts = set(value.split(","))
    elif isinstance(value, (list, tuple, set)):
        parts = set(value)
    else:
        raise PyYouTubeException(
            ErrorMessage(
                status_code=ErrorCode.INVALID_PARAMS,
                message=f"Parameter (parts) must be single str,comma-separated str,list,tuple or set",
            )
        )
    # check parts whether support.
    if check:
        support_parts = RESOURCE_PARTS_MAPPING[resource]
        if not support_parts.issuperset(parts):
            not_support_parts = ",".join(parts.difference(support_parts))
            raise PyYouTubeException(
                ErrorMessage(
                    status_code=ErrorCode.INVALID_PARAMS,
                    message=f"Parts {not_support_parts} for resource {resource} not support",
                )
            )
    return ",".join(parts)
