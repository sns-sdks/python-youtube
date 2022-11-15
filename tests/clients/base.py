"""
    Base class
"""


class BaseTestCase:
    BASE_PATH = "testdata/apidata"
    BASE_URL = "https://www.googleapis.com/youtube/v3"
    RESOURCE = "CHANNELS"

    @property
    def url(self):
        return f"{self.BASE_URL}/{self.RESOURCE}"

    def load_json(self, filename, helpers):
        return helpers.load_json(f"{self.BASE_PATH}/{filename}")
