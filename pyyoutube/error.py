from dataclasses import dataclass
from typing import Optional, Union

from requests import Response

__all__ = ["ErrorCode", "ErrorMessage", "PyYouTubeException"]


class ErrorCode:
    HTTP_ERROR = 10000
    MISSING_PARAMS = 10001
    INVALID_PARAMS = 10002
    NEED_AUTHORIZATION = 10003
    AUTHORIZE_URL_FIRST = 10004


@dataclass
class ErrorMessage:
    status_code: Optional[int] = None
    message: Optional[str] = None


class PyYouTubeException(Exception):
    """
    This is a return demo:
    {'error': {'errors': [{'domain': 'youtube.parameter',
    'reason': 'missingRequiredParameter',
    'message': 'No filter selected. Expected one of: forUsername, managedByMe, categoryId, mine, mySubscribers, id, idParam',
    'locationType': 'parameter',
    'location': ''}],
    'code': 400,
    'message': 'No filter selected. Expected one of: forUsername, managedByMe, categoryId, mine, mySubscribers, id, idParam'}}
    """

    def __init__(self, response: Optional[Union[ErrorMessage, Response]]):
        self.status_code: Optional[int] = None
        self.error_type: Optional[str] = None
        self.message: Optional[str] = None
        self.response: Optional[Union[ErrorMessage, Response]] = response
        self.error_handler()

    def error_handler(self):
        """
        Error has two big type(but not the error type.): This module's error, Api return error.
        So This will change two error to one format
        """
        if isinstance(self.response, ErrorMessage):
            self.status_code = self.response.status_code
            self.message = self.response.message
            self.error_type = "PyYouTubeException"
        elif isinstance(self.response, Response):
            res_data = self.response.json()
            if "error" in res_data:
                self.status_code = res_data["error"]["code"]
                self.message = res_data["error"]["message"]
                self.error_type = "YouTubeException"

    def __repr__(self):
        return (
            f"{self.error_type}(status_code={self.status_code},message={self.message})"
        )

    def __str__(self):
        return self.__repr__()
