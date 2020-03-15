Python YouTube

A Python wrapper around for YouTube Data API V3.

.. image:: https://travis-ci.org/sns-sdks/python-youtube.svg?branch=master
    :target: https://travis-ci.org/sns-sdks/python-youtube

.. image:: https://readthedocs.org/projects/python-youtube/badge/?version=latest
    :target: https://python-youtube.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://codecov.io/gh/sns-sdks/python-youtube/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/sns-sdks/python-youtube

.. image:: https://img.shields.io/pypi/v/python-youtube.svg
    :target: https://img.shields.io/pypi/v/python-youtube

======
THANKS
======

This project structure is base on `Python-Twitter <https://github.com/bear/python-twitter>`_.

Thanks a lot for Python-Twitter Developers.

============
Introduction
============

Library provides an easy way to use YouTube Data API V3.

=============
Documentation
=============

You can view the latest ``python-youtube`` documentation at: https://python-youtube.readthedocs.io/en/latest/.

Also view the full ``YouTube DATA API`` docs at: https://google-developers.appspot.com/youtube/v3/docs/.

==========
Installing
==========

You can install this lib from `pypi`::

    $pip install --upgrade python-youtube
    ✨🍰✨

=====
Using
=====

The API is exposed via the ``pyyoutube.Api`` class.

-----------
INSTANTIATE
-----------

There provide two method to create instance the ``pyyoutube.Api``.

You can just initialize with the an api key::

    In [1]: from pyyoutube import Api
    In [2]: api = Api(api_key='your api key')

If you want to get some authorization data. you need to initialize with an access token::

    In [1]: from pyyoutube import Api
    In [2]: api = Api(api_key='your api key')

You can read the docs to see how to get an access token.

Now you can use the instance to get data from YouTube.

------------
CHANNEL DATA
------------

Now library provide several ways to get channel's data.

If not found channel. the property ``items`` will return with blank list.

You can use channel id::

    In [3]: channel_by_id = api.get_channel_info(channel_id="UC_x5XG1OV2P6uZZ5FSM9Ttw")
    In [4]: channel_by_id.items
    Out[4]: [Channel(kind='youtube#channel', id='UC_x5XG1OV2P6uZZ5FSM9Ttw')]
    In [6]: channel_by_id.items[0].to_dict()
    Out[6]:
    {'kind': 'youtube#channel',
     'etag': '"j6xRRd8dTPVVptg711_CSPADRfg/AW8QEqbNRoIJv9KuzCIg0CG6aJA"',
     'id': 'UC_x5XG1OV2P6uZZ5FSM9Ttw',
     'snippet': {'title': 'Google Developers',
      'description': 'The Google Developers channel features talks from events, educational series, best practices, tips, and the latest updates across our products and platforms.',
      'customUrl': 'googlecode',
      'publishedAt': '2007-08-23T00:34:43.000Z',
      'thumbnails': {'default': {'url': 'https://yt3.ggpht.com/a/AGF-l78iFtAxyRZcUBzG91kbKMES19z-zGW5KT20_g=s88-c-k-c0xffffffff-no-rj-mo',
        'width': 88,
        'height': 88},
       'medium': {'url': 'https://yt3.ggpht.com/a/AGF-l78iFtAxyRZcUBzG91kbKMES19z-zGW5KT20_g=s240-c-k-c0xffffffff-no-rj-mo',
        'width': 240,
        'height': 240},
       'high': {'url': 'https://yt3.ggpht.com/a/AGF-l78iFtAxyRZcUBzG91kbKMES19z-zGW5KT20_g=s800-c-k-c0xffffffff-no-rj-mo',
        'width': 800,
        'height': 800},
       'standard': None,
       'maxres': None},
      'defaultLanguage': None,
      'localized': {'title': 'Google Developers',
       'description': 'The Google Developers channel features talks from events, educational series, best practices, tips, and the latest updates across our products and platforms.'},
      'country': 'US'},
      ...
      }

You can pass channel id with comma-separated id string or a list,tuple or set of ids to get multi channels.
Many methods also provide this method.

with ids::

    In [9]: channel_by_ids = api.get_channel_info(channel_id="UC_x5XG1OV2P6uZZ5FSM9Ttw,UCa-vrCLQHviTOVnEKDOdetQ")
    In [10]: channel_by_ids.items
    Out[10]:
    [Channel(kind='youtube#channel', id='UC_x5XG1OV2P6uZZ5FSM9Ttw'),
     Channel(kind='youtube#channel', id='UCa-vrCLQHviTOVnEKDOdetQ')]

You can also use channel name::

    In [7]: channel_by_name = api.get_channel_info(channel_name="GoogleDevelopers")
    In [8]: channel_by_name.items[0]
    Out[8]: Channel(kind='youtube#channel', id='UC_x5XG1OV2P6uZZ5FSM9Ttw')

If you have authorized, you can get your channels::

    In [3]: channel_by_mine = api_with_authorization.get_channel_info(mine=True)
    In [4]: channel_by_mine.items[0]
    Out[4]: Channel(kind='youtube#channel', id='UCa-vrCLQHviTOVnEKDOdetQ')

.. note::
    To get your channel, you must do authorize first, otherwise you will get error.

--------
PLAYLIST
--------

There provide methods to get playlists by playlist id, channel id or get your self playlists.

Get playlists by id::

    In [5]: playlists_by_id = api.get_playlist_by_id(playlist_id="PLOU2XLYxmsIKpaV8h0AGE05so0fAwwfTw")
    In [6]: playlists_by_id.items
    Out[6]: [Playlist(kind='youtube#playlist', id='PLOU2XLYxmsIKpaV8h0AGE05so0fAwwfTw')]

Get playlists by channel(If you want to get target channel all playlist, just provide the parameter ``count`` with ``None``)::

    In [3]: playlists_by_channel = api.get_playlists(channel_id="UC_x5XG1OV2P6uZZ5FSM9Ttw")
    In [4]: playlists_by_channel.items
    Out[4]:
    [Playlist(kind='youtube#playlist', id='PLOU2XLYxmsIKpaV8h0AGE05so0fAwwfTw'),
     Playlist(kind='youtube#playlist', id='PLOU2XLYxmsIJO83u2UmyC8ud41AvUnhgj'),
     Playlist(kind='youtube#playlist', id='PLOU2XLYxmsILfV1LiUhDjbh1jkFjQWrYB'),
     Playlist(kind='youtube#playlist', id='PLOU2XLYxmsIKNr3Wfhm8o0TSojW7hEPPY'),
     Playlist(kind='youtube#playlist', id='PLOU2XLYxmsIJ8ItHmK4bRlY4GCzMgXLAJ')]

Get your playlists(this need authorization)::

    In [7]: playlists_by_mine = api.get_playlists(mine=True)

-------------
PLAYLIST ITEM
-------------

Similar you can get playlist items by playlist item id or playlist id.

Get playlist items by id::

    In [11]: playlist_item_by_id = api.get_playlist_item_by_id(playlist_item_id="UExPVTJYTFl4bXNJS3BhVjhoMEFHRTA
    ...: 1c28wZkF3d2ZUdy41NkI0NEY2RDEwNTU3Q0M2")

    In [12]: playlist_item_by_id.items
    Out[12]: [PlaylistItem(kind='youtube#playlistItem', id='UExPVTJYTFl4bXNJS3BhVjhoMEFHRTA1c28wZkF3d2ZUdy41NkI0NEY2RDEwNTU3Q0M2')]


Get playlist items by playlist id(If you want to get target playlist all items, just provide the parameter ``count`` with ``None``)::

    In [8]: playlist_item_by_playlist = api.get_playlist_items(playlist_id="PLOU2XLYxmsIKpaV8h0AGE05so0fAwwfTw", count=2)

    In [10]: playlist_item_by_playlist.items
    Out[10]:
    [PlaylistItem(kind='youtube#playlistItem', id='UExPVTJYTFl4bXNJS3BhVjhoMEFHRTA1c28wZkF3d2ZUdy41NkI0NEY2RDEwNTU3Q0M2'),
     PlaylistItem(kind='youtube#playlistItem', id='UExPVTJYTFl4bXNJS3BhVjhoMEFHRTA1c28wZkF3d2ZUdy4yODlGNEE0NkRGMEEzMEQy')]
    In [13]: playlist_item_by_id.items[0].snippet.resourceId
    Out[13]: ResourceId(kind='youtube#video', videoId='CvTApw9X8aA')

-----
VIDEO
-----

You can get videos info by several methods.

Get videos by video id(s)::

    In [14]: video_by_id = api.get_video_by_id(video_id="CvTApw9X8aA")

    In [15]: video_by_id
    Out[15]: VideoListResponse(kind='youtube#videoListResponse')

    In [16]: video_by_id.items
    Out[16]: [Video(kind='youtube#video', id='CvTApw9X8aA')]


Get videos by chart(If you want to get all videos, just provide the parameter ``count`` with ``None``)::

    In [17]: video_by_chart = api.get_videos_by_chart(chart="mostPopular", region_code="US", count=2)

    In [18]: video_by_chart.items
    Out[18]:
    [Video(kind='youtube#video', id='RwnN2FVaHmw'),
     Video(kind='youtube#video', id='hDeuSfo_Ys0')]


Get videos by your rating(this need authorization, also if you want to get all videos, just provide the parameter ``count`` with ``None``)::

    In [25]: videos_by_rating = api.get_videos_by_myrating(rating="like", count=2)

--------------
COMMENT THREAD
--------------

You can get comment thread info by id or some filter.

Get comment thread by id(s)::

    In [9]: ct_by_id = api.get_comment_thread_by_id(comment_thread_id='Ugz097FRhsQy5CVhAjp4AaABAg,UgzhytyP79_Pwa
       ...: Dd4UB4AaABAg')

    In [10]: ct_by_id.items
    Out[10]:
    [CommentThread(kind='youtube#commentThread', id='Ugz097FRhsQy5CVhAjp4AaABAg'),
     CommentThread(kind='youtube#commentThread', id='UgzhytyP79_PwaDd4UB4AaABAg')]

Get all comment threads relate to channel(include comment threads for the channel's video, also if you want to get all comment threads, just provide the parameter ``count`` with ``None``)::

    In [19]: ct_by_all = api.get_comment_threads(all_to_channel_id="UC_x5XG1OV2P6uZZ5FSM9Ttw", count=2)

    In [20]: ct_by_all.items
    Out[20]:
    [CommentThread(kind='youtube#commentThread', id='UgwlB_Cza9WtzUWahYN4AaABAg'),
     CommentThread(kind='youtube#commentThread', id='UgyvoQJ2LsxCBwGEpMB4AaABAg')]

Get comment threads only for the channel(If you want to get all comment threads, just provide the parameter ``count`` with ``None``)::

    In [3]: ct_by_channel = api.get_comment_threads(channel_id="UC_x5XG1OV2P6uZZ5FSM9Ttw", count=2)

    In [4]: ct_by_channel.items
    Out[4]:
    [CommentThread(kind='youtube#commentThread', id='UgyUBI0HsgL9emxcZpR4AaABAg'),
     CommentThread(kind='youtube#commentThread', id='Ugzi3lkqDPfIOirGFLh4AaABAg')]

Get comment threads only for the video(If you want to get all comment threads, just provide the parameter ``count`` with ``None``)::

    In [5]: ct_by_video = api.get_comment_threads(video_id="D-lhorsDlUQ", count=2)

    In [6]: ct_by_video.items
    Out[6]:
    [CommentThread(kind='youtube#commentThread', id='UgydxWWoeA7F1OdqypJ4AaABAg'),
     CommentThread(kind='youtube#commentThread', id='UgxKREWxIgDrw8w2e_Z4AaABAg')]

-------
COMMENT
-------

You can get comment info by id or use the toplevel comment id to get replies.

.. note::
    The reply has the same structure as comment.

Get comments by id(s)::

    In [11]: comment_by_id = api.get_comment_by_id(comment_id='UgxKREWxIgDrw8w2e_Z4AaABAg,UgyrVQaFfEdvaSzstj14Aa
        ...: ABAg')

    In [12]: comment_by_id.items
    Out[12]:
    [Comment(kind='youtube#comment', id='UgxKREWxIgDrw8w2e_Z4AaABAg', snippet=CommentSnippet(authorDisplayName='Hieu Nguyen', likeCount=0)),
     Comment(kind='youtube#comment', id='UgyrVQaFfEdvaSzstj14AaABAg', snippet=CommentSnippet(authorDisplayName='Mani Kanta', likeCount=0))]

Get replies by comment id(If you want to get all comments, just provide the parameter ``count`` with ``None``)::

    In [13]: comment_by_parent = api.get_comments(parent_id="UgwYjZXfNCUTKPq9CZp4AaABAg")

    In [14]: comment_by_parent.items
    Out[14]: [Comment(kind='youtube#comment', id='UgwYjZXfNCUTKPq9CZp4AaABAg.8yxhlQJogG18yz_cXK9Kcj', snippet=CommentSnippet(authorDisplayName='Marlon López', likeCount=0))]

--------------
GUIDE CATEGORY
--------------

You can use category id or category belongs region's code to get guide categories.

Get guide categories with id(s)::

    In [16]: guide_category_by_id = api.get_guide_categories(category_id="GCQmVzdCBvZiBZb3VUdWJl,GCQ3JlYXRvciBvb
        ...: iB0aGUgUmlzZQ")

    In [17]: guide_category_by_id.items
    Out[17]:
    [GuideCategory(kind='youtube#guideCategory', id='GCQmVzdCBvZiBZb3VUdWJl'),
     GuideCategory(kind='youtube#guideCategory', id='GCQ3JlYXRvciBvbiB0aGUgUmlzZQ')]

Get guide categories with region code::

    In [19]: guide_categories_by_region = api.get_guide_categories(region_code="US")

    In [20]: guide_categories_by_region.items
    Out[20]:
    [GuideCategory(kind='youtube#guideCategory', id='GCQmVzdCBvZiBZb3VUdWJl'),
     GuideCategory(kind='youtube#guideCategory', id='GCQ3JlYXRvciBvbiB0aGUgUmlzZQ'),
     GuideCategory(kind='youtube#guideCategory', id='GCTXVzaWM'),
     GuideCategory(kind='youtube#guideCategory', id='GCQ29tZWR5'),
     GuideCategory(kind='youtube#guideCategory', id='GCRmlsbSAmIEVudGVydGFpbm1lbnQ'),
     GuideCategory(kind='youtube#guideCategory', id='GCR2FtaW5n'),
     GuideCategory(kind='youtube#guideCategory', id='GCQmVhdXR5ICYgRmFzaGlvbg'),
     GuideCategory(kind='youtube#guideCategory', id='GCU3BvcnRz'),
     GuideCategory(kind='youtube#guideCategory', id='GCVGVjaA'),
     GuideCategory(kind='youtube#guideCategory', id='GCQ29va2luZyAmIEhlYWx0aA'),
     GuideCategory(kind='youtube#guideCategory', id='GCTmV3cyAmIFBvbGl0aWNz')]


--------------
VIDEO CATEGORY
--------------

Similar to guide category. you can get video category with id or region.

Get video categories with id(s)::

    In [21]: video_category_by_id = api.get_video_categories(category_id="17,18")

    In [22]: video_category_by_id.items
    Out[22]:
    [VideoCategory(kind='youtube#videoCategory', id='17'),
     VideoCategory(kind='youtube#videoCategory', id='18')]

Get video categories with region code::

    In [23]: video_categories_by_region = api.get_video_categories(region_code="US")

    In [24]: video_categories_by_region.items
    Out[24]:
    [VideoCategory(kind='youtube#videoCategory', id='1'),
     VideoCategory(kind='youtube#videoCategory', id='2'),
     VideoCategory(kind='youtube#videoCategory', id='10'),
     VideoCategory(kind='youtube#videoCategory', id='15'),
     ...]

-------------
SUBSCRIPTIONS
-------------

You can get subscriptions info by id, by point channel or by yourself.

.. note::
    If you want to get the subscriptions not set to public. You need do authorization first and get the access token.
    You can see the demo `A demo for get my subscription <examples/subscription.py>`_.

Get subscriptions info by id(s), this need your token have the permission for the subscriptions belongs channel or user::

    In [6]: r = api.get_subscription_by_id(
       ...:     subscription_id=[
       ...:         "zqShTXi-2-Tx7TtwQqhCBwViE_j9IEgnmRmPnqJljxo",
       ...:         "zqShTXi-2-Rya5uUxEp3ZsPI3fZrFQnSXNQCwvHBGGo"])
    In [7]: r
    Out[7]: SubscriptionListResponse(kind='youtube#subscriptionListResponse')
    In [8]: r.items
    Out[8]:
    [Subscription(kind='youtube#subscription', id='zqShTXi-2-Tx7TtwQqhCBwViE_j9IEgnmRmPnqJljxo', snippet=SubscriptionSnippet(title='PyCon 2015', description='')),
     Subscription(kind='youtube#subscription', id='zqShTXi-2-Rya5uUxEp3ZsPI3fZrFQnSXNQCwvHBGGo', snippet=SubscriptionSnippet(title='ikaros-life', description='This is a test channel.'))]

Get yourself subscriptions, this need you do authorization first or give the authorized access token::

    In [9]: r = api.get_subscription_by_me(
       ...:     mine=True,
       ...:     parts=["id", "snippet"],
       ...:     count=2
       ...:)
    In [10]: r
    Out[10]: SubscriptionListResponse(kind='youtube#subscriptionListResponse')
    In [11]: r.items
    Out[11]:
    [Subscription(kind='youtube#subscription', id='zqShTXi-2-Tx7TtwQqhCBwtJ-Aho6DZeutqZiP4Q79Q', snippet=SubscriptionSnippet(title='Next Day Video', description='')),
     Subscription(kind='youtube#subscription', id='zqShTXi-2-Tx7TtwQqhCBwViE_j9IEgnmRmPnqJljxo', snippet=SubscriptionSnippet(title='PyCon 2015', description=''))]

Get public channel's subscriptions::

    In [12]: r = api.get_subscription_by_channel(
    ...:     channel_id="UCAuUUnT6oDeKwE6v1NGQxug",
    ...:     parts="id,snippet",
    ...:     count=2
    ...:     )
    In [13]: r
    Out[13]: SubscriptionListResponse(kind='youtube#subscriptionListResponse')
    In [14]: r.items
    Out[14]:
    [Subscription(kind='youtube#subscription', id='FMP3Mleijt-52zZDGkHtR5KhwkvCcdQKWWWIA1j5eGc', snippet=SubscriptionSnippet(title='TEDx Talks', description="TEDx is an international community that organizes TED-style events anywhere and everywhere -- celebrating locally-driven ideas and elevating them to a global stage. TEDx events are produced independently of TED conferences, each event curates speakers on their own, but based on TED's format and rules.\n\nFor more information on using TED for commercial purposes (e.g. employee learning, in a film, or in an online course), please submit a media request using the link below.")),
     Subscription(kind='youtube#subscription', id='FMP3Mleijt_ZKvy5M-HhRlsqI4wXY7VmP5g8lvmRhVU', snippet=SubscriptionSnippet(title='TED Residency', description='The TED Residency program is an incubator for breakthrough ideas. It is free and open to all via a semi-annual competitive application. Those chosen as TED Residents spend four months at TED headquarters in New York City, working on their idea. Selection criteria include the strength of their idea, their character, and their ability to bring a fresh perspective and positive contribution to the diverse TED community.'))]


----------
ACTIVITIES
----------

You can get activities by channel id. And can get your activities after you have done the authorize.

Get public channel activities::

    In [3]: r = api.get_activities_by_channel(channel_id="UC_x5XG1OV2P6uZZ5FSM9Ttw", count=2)
    In [4]: r
    Out[4]: ActivityListResponse(kind='youtube#activityListResponse')
    In [5]: r.items
    Out[5]:
    [Activity(kind='youtube#activity', id='MTUxNTc3NzM2MDAyODIxOTQxNDM0NjAwMA==', snippet=ActivitySnippet(title='2019 Year in Review - The Developer Show', description='Here to bring you the latest developer news from across Google this year is Developer Advocate Timothy Jordan. In this last week of the year, we’re taking a look back at some of the coolest and biggest announcements we covered in 2019! \n\nFollow Google Developers on Instagram → https://goo.gle/googledevs\n\nWatch more #DevShow → https://goo.gle/GDevShow\nSubscribe to Google Developers → https://goo.gle/developers')),
     Activity(kind='youtube#activity', id='MTUxNTc3MTI4NzIzODIxOTQxNDM0NzI4MA==', snippet=ActivitySnippet(title='GDE Promo - Lara Martin', description='Meet Lara Martin, a Flutter/Dart Google Developers Expert and get inspired by her journey. Watch now for a preview of her story! #GDESpotlights #IncludedWithGoogle\n\nLearn about the GDE program → https://goo.gle/2qWOvAy\n\nGoogle Developers Experts → https://goo.gle/GDE\nSubscribe to Google Developers → https://goo.gle/developers'))]


Get your activities::

    In [10]: r = api_with_token.get_activities_by_me()
    In [11]: r.items
    Out[11]:
    [Activity(kind='youtube#activity', id='MTUxNTc0OTk2MjI3NDE0MjYwMDY1NjAwODA=', snippet=ActivitySnippet(title='华山日出', description='冷冷的山头')),
     Activity(kind='youtube#activity', id='MTUxNTc0OTk1OTAyNDE0MjYwMDY1NTc2NDg=', snippet=ActivitySnippet(title='海上日出', description='美美美'))]

Get your video captions::

    In [12]: r = api.get_captions_by_video(video_id="oHR3wURdJ94", parts=["id", "snippet"])
    In [13]: r
    Out[13]: CaptionListResponse(kind='youtube#captionListResponse')
    In [14]: r.items
    Out[14]:
    [Caption(kind='youtube#caption', id='SwPOvp0r7kd9ttt_XhcHdZthMwXG7Z0I', snippet=CaptionSnippet(videoId='oHR3wURdJ94', lastUpdated='2020-01-14T09:40:49.981Z')),
     Caption(kind='youtube#caption', id='fPMuDm722CIRcUAT3NTPQHQZJZJxt39kU7JvrHk8Kzs=', snippet=CaptionSnippet(videoId='oHR3wURdJ94', lastUpdated='2020-01-14T09:39:46.991Z'))]


If you already have caption id(s), you can get video caption by id(s)::

    In [15]: r = api.get_captions_by_video(video_id="oHR3wURdJ94", parts=["id", "snippet"], caption_id="SwPOvp0r7kd9ttt_XhcHdZthMwXG7Z0I")
    In [16]: r
    Out[16]: CaptionListResponse(kind='youtube#captionListResponse')
    In [17]: r.items
    Out[17]: [Caption(kind='youtube#caption', id='SwPOvp0r7kd9ttt_XhcHdZthMwXG7Z0I', snippet=CaptionSnippet(videoId='oHR3wURdJ94', lastUpdated='2020-01-14T09:40:49.981Z'))]

----------------
CHANNEL SECTIONS
----------------

You can get channel sections by self id or belonged channel id or you self channel.

Get channel sections by channel id::

    In[18]: r = api.get_channel_sections_by_channel(channel_id="UC_x5XG1OV2P6uZZ5FSM9Ttw")
    In[19]: r
    Out[19]: ChannelSectionResponse(kind='youtube#channelSectionListResponse')
    In[20]: r.items
    Out[20]:
    [ChannelSection(kind='youtube#channelSection', id='UC_x5XG1OV2P6uZZ5FSM9Ttw.e-Fk7vMPqLE'),
     ChannelSection(kind='youtube#channelSection', id='UC_x5XG1OV2P6uZZ5FSM9Ttw.B8DTd9ZXJqM'),
     ChannelSection(kind='youtube#channelSection', id='UC_x5XG1OV2P6uZZ5FSM9Ttw.MfvRjkWLxgk'),
     ChannelSection(kind='youtube#channelSection', id='UC_x5XG1OV2P6uZZ5FSM9Ttw.fEjJOXRoWwg'),
     ChannelSection(kind='youtube#channelSection', id='UC_x5XG1OV2P6uZZ5FSM9Ttw.PvTmxDBxtLs'),
     ChannelSection(kind='youtube#channelSection', id='UC_x5XG1OV2P6uZZ5FSM9Ttw.pmcIOsL7s98'),
     ChannelSection(kind='youtube#channelSection', id='UC_x5XG1OV2P6uZZ5FSM9Ttw.c3r3vYf9uD0'),
     ChannelSection(kind='youtube#channelSection', id='UC_x5XG1OV2P6uZZ5FSM9Ttw.ZJpkBl-mXfM'),
     ChannelSection(kind='youtube#channelSection', id='UC_x5XG1OV2P6uZZ5FSM9Ttw.9_wU0qhEPR8'),
     ChannelSection(kind='youtube#channelSection', id='UC_x5XG1OV2P6uZZ5FSM9Ttw.npYvuMz0_es')]

Get authorize user's channel sections::

    In[21]: r = api.get_channel_sections_by_channel(mine=True)
    In[23]: r.items
    Out[23]:
    [ChannelSection(kind='youtube#channelSection', id='UCa-vrCLQHviTOVnEKDOdetQ.jNQXAC9IVRw'),
     ChannelSection(kind='youtube#channelSection', id='UCa-vrCLQHviTOVnEKDOdetQ.LeAltgu_pbM'),
     ChannelSection(kind='youtube#channelSection', id='UCa-vrCLQHviTOVnEKDOdetQ.nGzAI5pLbMY')]

Get channel section detail info by his id::

    In[24]: r = api.get_channel_section_by_id(section_id="UC_x5XG1OV2P6uZZ5FSM9Ttw.e-Fk7vMPqLE")
    In[25]: r
    Out[25]: ChannelSectionResponse(kind='youtube#channelSectionListResponse')
    In[26]: r1.items
    Out[26]: [ChannelSection(kind='youtube#channelSection', id='UC_x5XG1OV2P6uZZ5FSM9Ttw.e-Fk7vMPqLE')]

-------------
I18N RESOURCE
-------------

You can get a list of content regions that the YouTube website supports::

    In[27]: r = api.get_i18n_regions(parts=["snippet"])
    In[28]: r.items
    Out[28]:
    [I18nRegion(kind='youtube#i18nRegion', id='DZ', snippet=I18nRegionSnippet(gl='DZ', name='Algeria')),
     I18nRegion(kind='youtube#i18nRegion', id='AR', snippet=I18nRegionSnippet(gl='AR', name='Argentina')),
     I18nRegion(kind='youtube#i18nRegion', id='AU', snippet=I18nRegionSnippet(gl='AU', name='Australia'))
     ...]

You can get a list of application languages that the YouTube website supports::

    In[29]: r = api.get_i18n_languages(parts=["snippet"])
    In[30]: r.items
    Out[30]:
    [I18nLanguage(kind='youtube#i18nLanguage', id='af', snippet=I18nLanguageSnippet(hl='af', name='Afrikaans')),
     I18nLanguage(kind='youtube#i18nLanguage', id='az', snippet=I18nLanguageSnippet(hl='az', name='Azerbaijani')),
     I18nLanguage(kind='youtube#i18nLanguage', id='id', snippet=I18nLanguageSnippet(hl='id', name='Indonesian')),
     ...]

-------------------------
VIDEO ABUSE REPORT REASON
-------------------------

You can retrieve a list of reasons that can be used to report abusive videos::

    In[31]: r = api_with_token.get_video_abuse_report_reason(parts=["snippet"])
    In[32]: r.items
    Out[34]:
    [VideoAbuseReportReason(kind='youtube#videoAbuseReportReason'),
     VideoAbuseReportReason(kind='youtube#videoAbuseReportReason')]

------
SEARCH
------

You can use those methods to search the video,playlist,channel data. for more info, you can see the `Search Request Docs <https://developers.google.com/youtube/v3/docs/search/list>`_ .

You can search different type of resource with keywords::

    In[33]: r = api.search_by_keywords(q="surfing", search_type=["channel","video", "playlist"], count=5, limit=5)
    In[34]: r.items
    Out[34]:
    [SearchResult(kind='youtube#searchResult'),
     SearchResult(kind='youtube#searchResult'),
     SearchResult(kind='youtube#searchResult'),
     SearchResult(kind='youtube#searchResult'),
     SearchResult(kind='youtube#searchResult')]

You can search your app send videos::

    In[35]: r = api_with_token.search_by_developer(q="news", count=1)
    In[36]: r.items
    Out[36]:
    [SearchResult(kind='youtube#searchResult')]

You can search your videos::

    In[37]: r = api_with_token.search_by_mine(q="news", count=1)
    In[38]: r.items
    Out[39]:
    [SearchResult(kind='youtube#searchResult')]

Or you can build your request by ``search`` method, examples as follows::

    In[40]: r = api.search(
       ...:     location="21.5922529, -158.1147114",
       ...:     location_radius="10mi",
       ...:     q="surfing",
       ...:     parts=["snippet"],
       ...:     count=5,
       ...:     published_after="2020-02-01T00:00:00Z",
       ...:     published_before="2020-03-01T00:00:00Z",
       ...:     safe_search="moderate",
       ...:     search_type="video")
    In[41]: r.items
    Out[41]:
    [SearchResult(kind='youtube#searchResult'),
     SearchResult(kind='youtube#searchResult'),
     SearchResult(kind='youtube#searchResult'),
     SearchResult(kind='youtube#searchResult'),
     SearchResult(kind='youtube#searchResult')]

    In[42]: r = api.search(
       ...:     event_type="live",
       ...:     q="news",
       ...:     count=3,
       ...:     parts=["snippet"],
       ...:     search_type="video",
       ...:     topic_id="/m/09s1f",
       ...:     order="viewCount")
    In[43]: r.items
    Out[43]:
    [SearchResult(kind='youtube#searchResult'),
     SearchResult(kind='youtube#searchResult'),
     SearchResult(kind='youtube#searchResult')]

====
TODO
====

Now this has follows api.

- OAuth Demo
- Channel Info
- Playlist Info
- PlaylistItem Info
- Video Info
- Comment Thread Info
- Comment Info
- Video Categories Info
- Guide Categories Info
- Subscriptions Info
- Activities Info
- Captions Info
- Channel Sections Info
- Search Requests and simple usage.

Doing

- post or other method.