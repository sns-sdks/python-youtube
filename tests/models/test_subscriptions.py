import json
import unittest
import pyyoutube.models as models


class SubscriptionModelTest(unittest.TestCase):
    BASE_PATH = "testdata/modeldata/subscriptions/"

    with open(BASE_PATH + "snippet.json", "rb") as f:
        SNIPPETS = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "contentDetails.json", "rb") as f:
        CONTENT_DETAILS = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "subscriberSnippet.json", "rb") as f:
        SUBSCRIBER_SNIPPET = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "subscription.json", "rb") as f:
        SUBSCRIPTION_INFO = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "resp.json", "rb") as f:
        SUBSCRIPTION_RESPONSE = json.loads(f.read().decode("utf-8"))

    def testSubscriptionSnippet(self) -> None:
        m = models.SubscriptionSnippet.from_dict(self.SNIPPETS)

        self.assertEqual(m.channelId, "UCNvMBmCASzTNNX8lW3JRMbw")
        self.assertEqual(m.resourceId.channelId, "UCQ7dFBzZGlBvtU2hCecsBBg")
        self.assertEqual(
            m.thumbnails.default.url,
            "https://yt3.ggpht.com/s88-c-k-no-mo-rj-c0xffffff/photo.jpg",
        )

    def testSubscriptionContentDetails(self) -> None:
        m = models.SubscriptionContentDetails.from_dict(self.CONTENT_DETAILS)

        self.assertEqual(m.totalItemCount, 2)
        self.assertEqual(m.activityType, "all")

    def testSubscriptionSubscriberSnippet(self) -> None:
        m = models.SubscriptionSubscriberSnippet.from_dict(self.SUBSCRIBER_SNIPPET)

        self.assertEqual(m.title, "kun liu")
        self.assertEqual(
            m.thumbnails.default.url,
            "https://yt3.ggpht.com/s88-c-k-no-mo-rj-c0xffffff/photo.jpg",
        )

    def testSubscription(self) -> None:
        m = models.Subscription.from_dict(self.SUBSCRIPTION_INFO)

        self.assertEqual(m.id, "zqShTXi-2-Rya5uUxEp3ZsPI3fZrFQnSXNQCwvHBGGo")
        self.assertEqual(m.snippet.title, "ikaros-life")
        self.assertEqual(m.contentDetails.totalItemCount, 2)
        self.assertEqual(m.subscriberSnippet.title, "kun liu")

    def testSubscriptionResponse(self) -> None:
        m = models.SubscriptionListResponse.from_dict(self.SUBSCRIPTION_RESPONSE)

        self.assertEqual(m.nextPageToken, "CAUQAA")
        self.assertEqual(m.pageInfo.totalResults, 16)
        self.assertEqual(len(m.items), 5)
