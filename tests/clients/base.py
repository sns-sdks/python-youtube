class BaseTestCase:
    base_path = "testdata/apidata"
    base_url = "https://www.googleapis.com/youtube/v3"
    resource = "CHANNELS"

    @property
    def url(self):
        return f"{self.base_url}/{self.resource}"

    def load_json(self, filename, helpers):
        return helpers.load_json(f"{self.base_path}/{filename}")
