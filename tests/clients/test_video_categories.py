import pytest
import responses

from .base import BaseTestCase
from pyyoutube.error import PyYouTubeException


class TestVideoCategoriesResource(BaseTestCase):
    RESOURCE = "videoCategories"

    def test_list(self, helpers, key_cli):
        with pytest.raises(PyYouTubeException):
            key_cli.videoCategories.list()

        with responses.RequestsMock() as m:
            m.add(
                method="GET",
                url=self.url,
                json=self.load_json(
                    "categories/video_category_by_region.json", helpers
                ),
            )
            res = key_cli.videoCategories.list(
                parts=["snippet"],
                region_code="US",
            )
            assert res.items[0].snippet.title == "Film & Animation"

        with responses.RequestsMock() as m:
            m.add(
                method="GET",
                url=self.url,
                json=self.load_json("categories/video_category_multi.json", helpers),
            )
            res = key_cli.videoCategories.list(
                parts=["snippet"],
                category_id=["17", "18"],
            )
            assert len(res.items) == 2
