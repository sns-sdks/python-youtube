import responses

from .base import BaseTestCase


class TestSearchResource(BaseTestCase):
    RESOURCE = "search"

    def test_list(self, helpers, authed_cli, key_cli):
        with responses.RequestsMock() as m:
            m.add(
                method="GET",
                url=self.url,
                json=self.load_json("search/search_by_developer.json", helpers),
            )

            res = authed_cli.search.list(
                parts=["snippet"],
                for_content_owner=True,
            )
            assert res.items[0].id.videoId == "WuyFniRMrxY"

            res = authed_cli.search.list(
                for_developer=True,
                max_results=5,
            )
            assert len(res.items) == 5

        with responses.RequestsMock() as m:
            m.add(
                method="GET",
                url=self.url,
                json=self.load_json("search/search_by_mine.json", helpers),
            )
            res = authed_cli.search.list(for_mine=True, max_results=5)
            assert res.items[0].snippet.channelId == "UCa-vrCLQHviTOVnEKDOdetQ"

        with responses.RequestsMock() as m:
            m.add(
                method="GET",
                url=self.url,
                json=self.load_json("search/search_by_related_video.json", helpers),
            )
            res = authed_cli.search.list(
                related_to_video_id="Ks-_Mh1QhMc",
                region_code="US",
                relevance_language="en",
                safe_search="moderate",
                max_results=5,
            )
            assert res.items[0].id.videoId == "eIho2S0ZahI"

        with responses.RequestsMock() as m:
            m.add(
                method="GET",
                url=self.url,
                json=self.load_json("search/search_by_keywords_p1.json", helpers),
            )
            res = key_cli.search.list(
                q="surfing",
                parts=["snippet"],
                count=25,
            )
            assert len(res.items) == 25
