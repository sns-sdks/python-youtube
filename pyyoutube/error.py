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
        else:
            if 'error' in res:
                self.status_code = res['error']['code']
                self.message = res['error']['message']
                if 'errors' in res['error']:
                    self.error_type = res['error']['errors'][0]['reason']
