"""
    function's params checker.
"""

from pyyoutube.error import ErrorCode, ErrorMessage, PyYouTubeException
from pyyoutube.utils.constants import RESOURCE_PARTS_MAPPING


def comma_separated_validator(**kwargs):
    """
    Validate the param layout whether comma-separated string.

    Args:
        kwargs (str)
            Parameter need to do validate.

    Returns:
        None
    """
    for name, param in kwargs.items():
        if param is not None:
            try:
                param.split(",")
            except AttributeError:
                raise PyYouTubeException(
                    ErrorMessage(
                        status_code=ErrorCode.INVALID_PARAMS,
                        message=f"Parameter {name} must be str or comma-separated list str",
                    )
                )


def parts_validator(resource: str, parts: str):
    """
    Validate the resource whether support the parts.

    Args:
        resource (str)
            The YouTube resource string.
        parts (str)
            Parts need to do validate.
    Returns:
        True or False
    """
    if parts is not None:
        support_parts = RESOURCE_PARTS_MAPPING[resource]
        parts = set(parts.split(","))
        if not support_parts.issuperset(parts):
            not_support_parts = ",".join(parts.difference(support_parts))
            raise PyYouTubeException(
                ErrorMessage(
                    status_code=ErrorCode.INVALID_PARAMS,
                    message=f"Part {not_support_parts} for resource {resource} not support",
                )
            )


def incompatible_validator(**kwargs):
    """
    Validate the incompatible parameters.

    Args:
        kwargs (str)
            Parameter need to do validate.

    Returns:
        None
    """
    given = 0
    for name, param in kwargs.items():
        if param is not None:
            given += 1
    params = ",".join(kwargs.keys())
    if given == 0:
        raise PyYouTubeException(
            ErrorMessage(
                status_code=ErrorCode.MISSING_PARAMS,
                message=f"Specify at least one of {params}",
            )
        )
    elif given > 1:
        raise PyYouTubeException(
            ErrorMessage(
                status_code=ErrorCode.INVALID_PARAMS,
                message=f"Incompatible parameters specified for {params}",
            )
        )
