import unittest
import pyyoutube


class ModelTest(unittest.TestCase):
    SIMPLE_CHANNEL = {
        "kind": "youtube#channel",
        "etag": "\"XpPGQXPnxQJhLgs6enD_n8JR4Qk/iHSDLehwFV-BccJ-iP2PBCJkVyE\"",
        "id": "UC_x5XG1OV2P6uZZ5FSM9Ttw",
        "snippet": {
            "title": "Google Developers",
            "description": "The Google Developers channel features talks from events, educational series, best practices, tips, and the latest updates across our products and platforms.",
            "customUrl": "googledevelopers",
            "publishedAt": "2007-08-23T00:34:43.000Z",
            "thumbnails": {
                "default": {
                    "url": "https://yt3.ggpht.com/a-/AAuE7mAR_Pc0M1BkI4_Cjllw0VG3PJYs7ikMN1Avwg=s88-mo-c-c0xffffffff-rj-k-no",
                    "width": 88,
                    "height": 88
                },
                "medium": {
                    "url": "https://yt3.ggpht.com/a-/AAuE7mAR_Pc0M1BkI4_Cjllw0VG3PJYs7ikMN1Avwg=s240-mo-c-c0xffffffff-rj-k-no",
                    "width": 240,
                    "height": 240
                },
                "high": {
                    "url": "https://yt3.ggpht.com/a-/AAuE7mAR_Pc0M1BkI4_Cjllw0VG3PJYs7ikMN1Avwg=s800-mo-c-c0xffffffff-rj-k-no",
                    "width": 800,
                    "height": 800
                }
            },
            "localized": {
                "title": "Google Developers",
                "description": "The Google Developers channel features talks from events, educational series, best practices, tips, and the latest updates across our products and platforms."
            }
        },
        "contentDetails": {
            "relatedPlaylists": {
                "uploads": "UU_x5XG1OV2P6uZZ5FSM9Ttw",
                "watchHistory": "HL",
                "watchLater": "WL"
            }
        },
        "statistics": {
            "viewCount": "150564102",
            "commentCount": "0",
            "subscriberCount": "1767680",
            "hiddenSubscriberCount": False,
            "videoCount": "4879"
        },
        "topicDetails": {
            "topicIds": [
                "/m/07c1v",
                "/m/019_rr"
            ],
            "topicCategories": [
                "https://en.wikipedia.org/wiki/Technology",
                "https://en.wikipedia.org/wiki/Lifestyle_(sociology)"
            ]
        },
        "status": {
            "privacyStatus": "public",
            "isLinked": True,
            "longUploadsStatus": "longUploadsUnspecified"
        },
        "brandingSettings": {
            "channel": {
                "title": "Google Developers",
                "description": "The Google Developers channel features talks from events, educational series, best practices, tips, and the latest updates across our products and platforms.",
                "defaultTab": "Featured",
                "trackingAnalyticsAccountId": "YT-9170156-1",
                "moderateComments": True,
                "showRelatedChannels": True,
                "showBrowseView": True,
                "featuredChannelsTitle": "Featured Channels",
                "featuredChannelsUrls": [
                    "UCP4bf6IHJJQehibu6ai__cg",
                    "UCVHFbqXqoYvEWM1Ddxl0QDg",
                    "UCnUYZLuoy1rq1aVMwx4aTzw",
                    "UClKO7be7O9cUGL94PHnAeOA",
                    "UCdIiCSqXuybzwGwJwrpHPqw",
                    "UCJS9pqu9BzkAMNTmzNMNhvg",
                    "UCorTyjVGM-PV5CCKbosONow",
                    "UCTspylBf8iNobZHgwUD4PXA",
                    "UCeo-MamuQVFRcfQmS2N7fhw",
                    "UCQqa5UIHtrnpiADC3eHFupw",
                    "UCXPBsjgKKG2HqsKBhWA4uQw"
                ],
                "unsubscribedTrailer": "Ou-gulnNkaE",
                "profileColor": "#000000"
            },
            "image": {
                "bannerImageUrl": "https://yt3.ggpht.com/7KFMbsdBCYGZqbg3lYNcxpDQpwoHgwSH8aRtUp7xUBda_uHxTVZXNzBHFgiBMp_ZjfHpfn4TeQ=w1060-fcrop64=1,00005a57ffffa5a8-nd-c0xffffffff-rj-k-no",
                "bannerMobileImageUrl": "https://yt3.ggpht.com/7KFMbsdBCYGZqbg3lYNcxpDQpwoHgwSH8aRtUp7xUBda_uHxTVZXNzBHFgiBMp_ZjfHpfn4TeQ=w640-fcrop64=1,32b75a57cd48a5a8-nd-c0xffffffff-rj-k-no",
                "bannerTabletLowImageUrl": "https://yt3.ggpht.com/7KFMbsdBCYGZqbg3lYNcxpDQpwoHgwSH8aRtUp7xUBda_uHxTVZXNzBHFgiBMp_ZjfHpfn4TeQ=w1138-fcrop64=1,00005a57ffffa5a8-nd-c0xffffffff-rj-k-no",
                "bannerTabletImageUrl": "https://yt3.ggpht.com/7KFMbsdBCYGZqbg3lYNcxpDQpwoHgwSH8aRtUp7xUBda_uHxTVZXNzBHFgiBMp_ZjfHpfn4TeQ=w1707-fcrop64=1,00005a57ffffa5a8-nd-c0xffffffff-rj-k-no",
                "bannerTabletHdImageUrl": "https://yt3.ggpht.com/7KFMbsdBCYGZqbg3lYNcxpDQpwoHgwSH8aRtUp7xUBda_uHxTVZXNzBHFgiBMp_ZjfHpfn4TeQ=w2276-fcrop64=1,00005a57ffffa5a8-nd-c0xffffffff-rj-k-no",
                "bannerTabletExtraHdImageUrl": "https://yt3.ggpht.com/7KFMbsdBCYGZqbg3lYNcxpDQpwoHgwSH8aRtUp7xUBda_uHxTVZXNzBHFgiBMp_ZjfHpfn4TeQ=w2560-fcrop64=1,00005a57ffffa5a8-nd-c0xffffffff-rj-k-no",
                "bannerMobileLowImageUrl": "https://yt3.ggpht.com/7KFMbsdBCYGZqbg3lYNcxpDQpwoHgwSH8aRtUp7xUBda_uHxTVZXNzBHFgiBMp_ZjfHpfn4TeQ=w320-fcrop64=1,32b75a57cd48a5a8-nd-c0xffffffff-rj-k-no",
                "bannerMobileMediumHdImageUrl": "https://yt3.ggpht.com/7KFMbsdBCYGZqbg3lYNcxpDQpwoHgwSH8aRtUp7xUBda_uHxTVZXNzBHFgiBMp_ZjfHpfn4TeQ=w960-fcrop64=1,32b75a57cd48a5a8-nd-c0xffffffff-rj-k-no",
                "bannerMobileHdImageUrl": "https://yt3.ggpht.com/7KFMbsdBCYGZqbg3lYNcxpDQpwoHgwSH8aRtUp7xUBda_uHxTVZXNzBHFgiBMp_ZjfHpfn4TeQ=w1280-fcrop64=1,32b75a57cd48a5a8-nd-c0xffffffff-rj-k-no",
                "bannerMobileExtraHdImageUrl": "https://yt3.ggpht.com/7KFMbsdBCYGZqbg3lYNcxpDQpwoHgwSH8aRtUp7xUBda_uHxTVZXNzBHFgiBMp_ZjfHpfn4TeQ=w1440-fcrop64=1,32b75a57cd48a5a8-nd-c0xffffffff-rj-k-no",
                "bannerTvImageUrl": "https://yt3.ggpht.com/7KFMbsdBCYGZqbg3lYNcxpDQpwoHgwSH8aRtUp7xUBda_uHxTVZXNzBHFgiBMp_ZjfHpfn4TeQ=w2120-fcrop64=1,00000000ffffffff-nd-c0xffffffff-rj-k-no",
                "bannerTvLowImageUrl": "https://yt3.ggpht.com/7KFMbsdBCYGZqbg3lYNcxpDQpwoHgwSH8aRtUp7xUBda_uHxTVZXNzBHFgiBMp_ZjfHpfn4TeQ=w854-fcrop64=1,00000000ffffffff-nd-c0xffffffff-rj-k-no",
                "bannerTvMediumImageUrl": "https://yt3.ggpht.com/7KFMbsdBCYGZqbg3lYNcxpDQpwoHgwSH8aRtUp7xUBda_uHxTVZXNzBHFgiBMp_ZjfHpfn4TeQ=w1280-fcrop64=1,00000000ffffffff-nd-c0xffffffff-rj-k-no",
                "bannerTvHighImageUrl": "https://yt3.ggpht.com/7KFMbsdBCYGZqbg3lYNcxpDQpwoHgwSH8aRtUp7xUBda_uHxTVZXNzBHFgiBMp_ZjfHpfn4TeQ=w1920-fcrop64=1,00000000ffffffff-nd-c0xffffffff-rj-k-no"
            },
            "hints": [
                {
                    "property": "channel.banner.mobile.medium.image.url",
                    "value": "https://yt3.ggpht.com/7KFMbsdBCYGZqbg3lYNcxpDQpwoHgwSH8aRtUp7xUBda_uHxTVZXNzBHFgiBMp_ZjfHpfn4TeQ=w640-fcrop64=1,32b75a57cd48a5a8-nd-c0xffffffff-rj-k-no"
                },
                {
                    "property": "channel.featured_tab.template.string",
                    "value": "Everything"
                }
            ]
        }}

    def testChannel(self):
        m = pyyoutube.Channel.new_from_json_dict(self.SIMPLE_CHANNEL)
        self.assertEqual(type(m), pyyoutube.Channel)
