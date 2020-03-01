import json
import unittest

import responses
import pyyoutube


class ApiI18nTest(unittest.TestCase):
    BASE_PATH = "testdata/apidata/i18ns/"
    REGION_URL = "https://www.googleapis.com/youtube/v3/i18nRegions"
    LANGUAGE_URL = "https://www.googleapis.com/youtube/v3/i18nLanguages"

    with open(BASE_PATH + "regions_res.json", "rb") as f:
        REGIONS_RES = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "language_res.json", "rb") as f:
        LANGUAGE_RES = json.loads(f.read().decode("utf-8"))

    def setUp(self) -> None:
        self.api = pyyoutube.Api(api_key="api key")

    def testGetI18nRegions(self) -> None:
        with responses.RequestsMock() as m:
            m.add("GET", self.REGION_URL, json=self.REGIONS_RES)

            regions = self.api.get_i18n_regions(parts=["id", "snippet"])
            self.assertEqual(regions.kind, "youtube#i18nRegionListResponse")
            self.assertEqual(len(regions.items), 4)
            self.assertEqual(regions.items[0].id, "VE")

            regions_json = self.api.get_i18n_regions(return_json=True)
            self.assertEqual(len(regions_json["items"]), 4)

    def testGetI18nLanguages(self) -> None:
        with responses.RequestsMock() as m:
            m.add("GET", self.LANGUAGE_URL, json=self.LANGUAGE_RES)

            languages = self.api.get_i18n_languages(parts=["id", "snippet"])
            self.assertEqual(len(languages.items), 5)
            self.assertEqual(languages.items[0].id, "zh-CN")

            languages_json = self.api.get_i18n_languages(return_json=True)
            self.assertEqual(len(languages_json["items"]), 5)
