"""
    These are some decorators for params check and so on.
"""
from functools import wraps
from typing import List, Callable

from pyyoutube.error import ErrorCode, ErrorMessage, PyYouTubeException
from .constants import RESOURCE_PARTS_MAPPING


def incompatible(params: List[str]) -> Callable:
    """
    Validate the incompatible parameters.

    Args:
        params (list, Optional)
            Params list which need to check incompatible
    Returns:
        decorator
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            given = 0
            for param in params:
                if kwargs.get(param) is not None:
                    given += 1
            params_str = ",".join(params)
            if given == 0:
                raise PyYouTubeException(
                    ErrorMessage(
                        status_code=ErrorCode.INVALID_PARAMS,
                        message=f"Specify at least one of ({params_str})",
                    )
                )
            elif given > 1:
                raise PyYouTubeException(
                    ErrorMessage(
                        status_code=ErrorCode.INVALID_PARAMS,
                        message=f"Incompatible parameters specified for ({params_str})",
                    )
                )
            return func(*args, **kwargs)

        return wrapper

    return decorator


def parts_validator(*, resource: str) -> Callable:
    """
    Validate the resource whether support the parts.

    Args:
        resource (str)
            YouTube resource such as `channel`.
    Returns:
        decorator
    """

    def decorator(func):
        @wraps(func)
        def wrapper(**kwargs):
            parts = kwargs.get("parts")
            if parts is not None:
                if isinstance(parts, str):
                    parts = set(parts.split(","))
                elif isinstance(parts, (list, tuple, set)):
                    parts = set(parts)
                else:
                    raise PyYouTubeException(
                        ErrorMessage(
                            status_code=ErrorCode.INVALID_PARAMS,
                            message=f"Parts param only support list,set,tuple and comma-separated string",
                        )
                    )
                support_parts = RESOURCE_PARTS_MAPPING[resource]
                if not support_parts.issuperset(parts):
                    not_support_parts = ",".join(parts.difference(support_parts))
                    raise PyYouTubeException(
                        ErrorMessage(
                            status_code=ErrorCode.INVALID_PARAMS,
                            message=f"Not support parts ({not_support_parts}) for resource ({resource})",
                        )
                    )
            else:
                parts = RESOURCE_PARTS_MAPPING[resource]
            kwargs["parts"] = parts
            return func(**kwargs)

        return wrapper

    return decorator
