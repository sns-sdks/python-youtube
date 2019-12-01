import json
import unittest

import pyyoutube.models as models


class CommentModelModelTest(unittest.TestCase):
    BASE_PATH = "testdata/modeldata/comments/"

    with open(BASE_PATH + "comment_snippet.json", "rb") as f:
        SNIPPET_INFO = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "comment_info.json", "rb") as f:
        COMMENT_INFO = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "comment_api_response.json", "rb") as f:
        COMMENT_API_INFO = json.loads(f.read().decode("utf-8"))

    def testCommentSnippet(self) -> None:
        m = models.CommentSnippet.from_dict(self.SNIPPET_INFO)

        self.assertEqual(m.videoId, "wtLJPvx7-ys")
        self.assertTrue(m.canRate)
        self.assertEqual(m.authorChannelId.value, "UCqPku3cxM-ED3poX8YtGqeg")
        self.assertEqual(
            m.string_to_datetime(m.publishedAt).isoformat(), "2019-03-28T11:33:46+00:00"
        )

    def testComment(self) -> None:
        m = models.Comment.from_dict(self.COMMENT_INFO)

        self.assertEqual(m.id, "UgwxApqcfzZzF_C5Zqx4AaABAg")
        self.assertEqual(m.snippet.authorDisplayName, "Oeurn Ravuth")
        self.assertEqual(
            m.snippet.string_to_datetime(m.snippet.updatedAt).isoformat(),
            "2019-03-28T11:33:46+00:00",
        )

    def testCommentListResponse(self) -> None:
        m = models.CommentListResponse.from_dict(self.COMMENT_API_INFO)

        self.assertEqual(m.kind, "youtube#commentListResponse")
        self.assertEqual(m.items[0].id, "UgxKREWxIgDrw8w2e_Z4AaABAg")


class CommentThreadModelTest(unittest.TestCase):
    BASE_PATH = "testdata/modeldata/comments/"

    with open(BASE_PATH + "comment_thread_snippet.json", "rb") as f:
        SNIPPET_INFO = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "comment_thread_replies.json", "rb") as f:
        REPLIES_INFO = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "comment_thread_info.json", "rb") as f:
        COMMENT_THREAD_INFO = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "comment_thread_api_response.json", "rb") as f:
        COMMENT_THREAD_API_INFO = json.loads(f.read().decode("utf-8"))

    def testCommentThreadSnippet(self) -> None:
        m = models.CommentThreadSnippet.from_dict(self.SNIPPET_INFO)

        self.assertEqual(m.videoId, "D-lhorsDlUQ")
        self.assertEqual(m.topLevelComment.id, "UgydxWWoeA7F1OdqypJ4AaABAg")
        self.assertEqual(m.topLevelComment.snippet.videoId, "D-lhorsDlUQ")

    def testCommentThreadReplies(self) -> None:
        m = models.CommentThreadReplies.from_dict(self.REPLIES_INFO)

        self.assertEqual(len(m.comments), 1)
        self.assertEqual(
            m.comments[0].id, "UgydxWWoeA7F1OdqypJ4AaABAg.8wWQ3tdHcFx8xcDheui-qb"
        )
        self.assertEqual(m.comments[0].snippet.videoId, "D-lhorsDlUQ")

    def testCommentThread(self) -> None:
        m = models.CommentThread.from_dict(self.COMMENT_THREAD_INFO)

        self.assertEqual(m.id, "UgydxWWoeA7F1OdqypJ4AaABAg")
        self.assertEqual(m.snippet.videoId, "D-lhorsDlUQ")
        self.assertEqual(
            m.replies.comments[0].id,
            "UgydxWWoeA7F1OdqypJ4AaABAg.8wWQ3tdHcFx8xcDheui-qb",
        )

    def testCommentThreadListResponse(self) -> None:
        m = models.CommentThreadListResponse.from_dict(self.COMMENT_THREAD_API_INFO)

        self.assertEqual(m.kind, "youtube#commentThreadListResponse")
        self.assertEqual(m.items[0].id, "Ugz097FRhsQy5CVhAjp4AaABAg")
