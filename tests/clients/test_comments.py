import pytest
import responses

import pyyoutube.models as mds
from .base import BaseTestCase
from pyyoutube.error import PyYouTubeException


class TestCommentsResource(BaseTestCase):
    RESOURCE = "comments"

    def test_list(self, helpers, key_cli):
        with pytest.raises(PyYouTubeException):
            key_cli.comments.list()

        with responses.RequestsMock() as m:
            m.add(
                method="GET",
                url=self.url,
                json=self.load_json(
                    "comments/comments_by_parent_paged_1.json", helpers
                ),
            )
            res = key_cli.comments.list(
                parts=["id", "snippet"],
                parent_id="Ugw5zYU6n9pmIgAZWvN4AaABAg",
            )
            assert (
                res.items[0].id == "Ugw5zYU6n9pmIgAZWvN4AaABAg.91zT3cYb5B291za6voUoRh"
            )
            assert res.items[0].snippet.parentId == "Ugw5zYU6n9pmIgAZWvN4AaABAg"

            res = key_cli.comments.list(
                parts=["id", "snippet"],
                comment_id="UgyUBI0HsgL9emxcZpR4AaABAg,Ugzi3lkqDPfIOirGFLh4AaABAg",
            )
            assert len(res.items) == 2

    def test_insert(self, helpers, authed_cli):
        with responses.RequestsMock() as m:
            m.add(
                method="POST",
                url=self.url,
                json=self.load_json("comments/insert_response.json", helpers),
            )

            comment = authed_cli.comments.insert(
                body=mds.Comment(
                    snippet=mds.CommentSnippet(
                        parentId="Ugy_CAftKrIUCyPr9GR4AaABAg",
                        textOriginal="wow",
                    )
                ),
                parts=["id", "snippet"],
            )
            assert comment.snippet.parentId == "Ugy_CAftKrIUCyPr9GR4AaABAg"

    def test_update(self, helpers, authed_cli):
        with responses.RequestsMock() as m:
            m.add(
                method="PUT",
                url=self.url,
                json=self.load_json("comments/insert_response.json", helpers),
            )
            comment = authed_cli.comments.update(
                body=mds.Comment(
                    id="Ugy_CAftKrIUCyPr9GR4AaABAg.9iPXEClD9lW9iPXLqKy_Pt",
                    snippet=mds.CommentSnippet(
                        textOriginal="wow",
                    ),
                ),
                parts=["id", "snippet"],
            )
            assert comment.snippet.parentId == "Ugy_CAftKrIUCyPr9GR4AaABAg"

    def test_mark_as_spam(self, helpers, authed_cli):
        with responses.RequestsMock() as m:
            m.add(method="POST", url=f"{self.url}/markAsSpam", status=204)

            assert authed_cli.comments.mark_as_spam(
                comment_id="Ugy_CAftKrIUCyPr9GR4AaABAg.9iPXEClD9lW9iPXLqKy_Pt",
            )

        with pytest.raises(PyYouTubeException):
            with responses.RequestsMock() as m:
                m.add(
                    method="POST",
                    url=f"{self.url}/markAsSpam",
                    json=self.load_json("error_permission_resp.json", helpers),
                    status=403,
                )
                authed_cli.comments.mark_as_spam(
                    comment_id="Ugy_CAftKrIUCyPr9GR4AaABAg.9iPXEClD9lW9iPXLqKy_Pt",
                )

    def test_set_moderation_status(self, helpers, authed_cli):
        with responses.RequestsMock() as m:
            m.add(method="POST", url=f"{self.url}/setModerationStatus", status=204)

            assert authed_cli.comments.set_moderation_status(
                comment_id="Ugy_CAftKrIUCyPr9GR4AaABAg.9iPXEClD9lW9iPXLqKy_Pt",
                moderation_status="rejected",
            )

        with pytest.raises(PyYouTubeException):
            with responses.RequestsMock() as m:
                m.add(
                    method="POST",
                    url=f"{self.url}/setModerationStatus",
                    json=self.load_json("error_permission_resp.json", helpers),
                    status=403,
                )
                authed_cli.comments.set_moderation_status(
                    comment_id="Ugy_CAftKrIUCyPr9GR4AaABAg.9iPXEClD9lW9iPXLqKy_Pt",
                    moderation_status="published",
                    ban_author=True,
                )

    def test_delete(self, helpers, authed_cli):
        with responses.RequestsMock() as m:
            m.add(method="DELETE", url=f"{self.url}", status=204)

            assert authed_cli.comments.delete(
                comment_id="Ugy_CAftKrIUCyPr9GR4AaABAg.9iPXEClD9lW9iPXLqKy_Pt",
            )

        with pytest.raises(PyYouTubeException):
            with responses.RequestsMock() as m:
                m.add(
                    method="DELETE",
                    url=f"{self.url}",
                    json=self.load_json("error_permission_resp.json", helpers),
                    status=403,
                )
                authed_cli.comments.delete(
                    comment_id="Ugy_CAftKrIUCyPr9GR4AaABAg.9iPXEClD9lW9iPXLqKy_Pt",
                )
