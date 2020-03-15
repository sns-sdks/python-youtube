import json
import unittest

import pyyoutube.models as models


class SearchResultModelTest(unittest.TestCase):
    BASE_PATH = "testdata/modeldata/search_result/"

    with open(BASE_PATH + "search_result_id.json", "rb") as f:
        SEARCH_RES_ID_INFO = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "search_result_snippet.json", "rb") as f:
        SEARCH_RES_SNIPPET_INFO = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "search_result.json", "rb") as f:
        SEARCH_RES_INFO = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "search_result_api_response.json", "rb") as f:
        SEARCH_RES_API_INFO = json.loads(f.read().decode("utf-8"))

    def testSearchResultId(self):
        m = models.SearchResultId.from_dict(self.SEARCH_RES_ID_INFO)
        self.assertEqual(m.kind, "youtube#playlist")

    def testSearchResultSnippet(self):
        m = models.SearchResultSnippet.from_dict(self.SEARCH_RES_SNIPPET_INFO)

        self.assertEqual(m.channelId, "UC_x5XG1OV2P6uZZ5FSM9Ttw")
        self.assertEqual(
            m.string_to_datetime(m.publishedAt).isoformat(),
            "2016-03-30T16:59:12+00:00",
        )
        self.assertEqual(
            m.thumbnails.default.url, "https://i.ytimg.com/vi/cKxRvEZd3Mw/default.jpg"
        )

    def testSearchResult(self):
        m = models.SearchResult.from_dict(self.SEARCH_RES_INFO)
        self.assertEqual(m.kind, "youtube#searchResult")
        self.assertEqual(m.id.videoId, "fq4N0hgOWzU")

    def testSearchListResponse(self):
        m = models.SearchListResponse.from_dict(self.SEARCH_RES_API_INFO)

        self.assertEqual(m.kind, "youtube#searchListResponse")
        self.assertEqual(m.regionCode, "US")
        self.assertEqual(m.pageInfo.totalResults, 489126)
        self.assertEqual(len(m.items), 5)
