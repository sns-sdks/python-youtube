import pytest
import responses

import pyyoutube.models as mds
from .base import BaseTestCase
from pyyoutube.error import PyYouTubeException


class TestCommentThreadsResource(BaseTestCase):
    RESOURCE = "commentThreads"

    def test_list(self, helpers, key_cli):
        with pytest.raises(PyYouTubeException):
            key_cli.commentThreads.list()

        with responses.RequestsMock() as m:
            m.add(
                method="GET",
                url=self.url,
                json=self.load_json(
                    "comment_threads/comment_threads_by_video_paged_1.json", helpers
                ),
            )

            res = key_cli.commentThreads.list(
                parts=["id", "snippet"],
                all_threads_related_to_channel_id="UC_x5XG1OV2P6uZZ5FSM9Ttw",
            )
            assert res.items[0].snippet.totalReplyCount == 0

            res = key_cli.commentThreads.list(
                parts=["id", "snippet"],
                channel_id="UC_x5XG1OV2P6uZZ5FSM9Ttw",
            )
            assert res.items[0].snippet.totalReplyCount == 0

            res = key_cli.commentThreads.list(
                parts=["id", "snippet"],
                video_id="F1UP7wRCPH8",
            )
            assert res.items[0].snippet.videoId == "F1UP7wRCPH8"

            res = key_cli.commentThreads.list(
                parts=["id", "snippet"],
                thread_id="UgyZ1jqkHKYvi1-ruOZ4AaABAg,Ugy4OzAuz5uJuFt3FH54AaABAg",
            )
            assert res.items[0].id == "UgyZ1jqkHKYvi1-ruOZ4AaABAg"

    def test_insert(self, helpers, authed_cli):
        with responses.RequestsMock() as m:
            m.add(
                method="POST",
                url=self.url,
                json=self.load_json("comment_threads/insert_response.json", helpers),
            )

            thread = authed_cli.commentThreads.insert(
                body=mds.CommentThread(
                    snippet=mds.CommentThreadSnippet(
                        videoId="JE8xdDp5B8Q",
                        topLevelComment=mds.Comment(
                            snippet=mds.CommentSnippet(
                                textOriginal="Sun from the api",
                            )
                        ),
                    )
                ),
                parts=["id", "snippet"],
            )
            assert thread.snippet.videoId == "JE8xdDp5B8Q"
