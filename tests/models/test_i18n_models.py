import json

import unittest

import pyyoutube.models as models


class I18nModelTest(unittest.TestCase):
    BASE_PATH = "testdata/modeldata/i18ns/"

    with open(BASE_PATH + "region_info.json", "rb") as f:
        REGION_INFO = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "region_res.json", "rb") as f:
        REGION_RES = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "language_info.json", "rb") as f:
        LANGUAGE_INFO = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "language_res.json", "rb") as f:
        LANGUAGE_RES = json.loads(f.read().decode("utf-8"))

    def testI18nRegion(self) -> None:
        m = models.I18nRegion.from_dict(self.REGION_INFO)

        self.assertEqual(m.id, "DZ")
        self.assertEqual(m.snippet.gl, "DZ")

    def testI18nRegionResponse(self) -> None:
        m = models.I18nRegionListResponse.from_dict(self.REGION_RES)

        self.assertEqual(m.kind, "youtube#i18nRegionListResponse")
        self.assertEqual(len(m.items), 2)

    def testI18nLanguage(self) -> None:
        m = models.I18nLanguage.from_dict(self.LANGUAGE_INFO)

        self.assertEqual(m.id, "af")
        self.assertEqual(m.snippet.hl, "af")

    def testI18nLanguageResponse(self) -> None:
        m = models.I18nRegionListResponse.from_dict(self.LANGUAGE_RES)

        self.assertEqual(m.kind, "youtube#i18nLanguageListResponse")
        self.assertEqual(len(m.items), 2)
