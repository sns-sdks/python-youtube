from collections import namedtuple

ErrorMessage = namedtuple(
    'ErrorMessage',
    'status_code message'
)


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

    def __init__(self, response):
        self.status_code = None
        self.error_type = None
        self.message = None
        self.response = response
        self.error_handler()

    def error_handler(self):
        """
        Error has two big type(but not the error type.): This module's error, Api return error.
        So This will change two error to one format
        """
        res = getattr(self.response, 'json', None)
        if res is None:
            self.status_code = self.response.status_code
            self.message = self.response.message
            self.error_type = 'PyYouTubeException'
        elif callable(res):
            error_data = res()
            if 'error' in error_data:
                self.status_code = error_data['error']['code']
                self.message = error_data['error']['message']
                if 'errors' in error_data['error']:
                    self.error_type = error_data['error']['errors'][0]['reason']

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f'PyYouTubeException(status_code={self.status_code}, message={self.message})'
