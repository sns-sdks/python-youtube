import responses

from .base import BaseTestCase


class TestI18nLanguagesResource(BaseTestCase):
    RESOURCE = "i18nLanguages"

    def test_list(self, helpers, key_cli):
        with responses.RequestsMock() as m:
            m.add(
                method="GET",
                url=self.url,
                json=self.load_json("i18ns/language_res.json", helpers),
            )
            res = key_cli.i18nLanguages.list(
                parts=["snippet"],
            )
            assert res.items[0].snippet.name == "Chinese"


class TestI18nRegionsResource(BaseTestCase):
    RESOURCE = "i18nRegions"

    def test_list(self, helpers, key_cli):
        with responses.RequestsMock() as m:
            m.add(
                method="GET",
                url=self.url,
                json=self.load_json("i18ns/regions_res.json", helpers),
            )
            res = key_cli.i18nRegions.list(
                parts=["snippet"],
            )
            assert res.items[0].snippet.name == "Venezuela"
