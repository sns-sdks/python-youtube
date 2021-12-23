Python YouTube

A Python wrapper around for YouTube Data API V3.

.. image:: https://github.com/sns-sdks/python-youtube/workflows/Test/badge.svg
    :target: https://github.com/sns-sdks/python-youtube/actions

.. image:: https://img.shields.io/badge/Docs-passing-brightgreen
    :target: https://sns-sdks.github.io/python-youtube/
    :alt: Documentation Status

.. image:: https://codecov.io/gh/sns-sdks/python-youtube/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/sns-sdks/python-youtube

.. image:: https://img.shields.io/pypi/v/python-youtube.svg
    :target: https://img.shields.io/pypi/v/python-youtube

======
THANKS
======

Inspired by `Python-Twitter <https://github.com/bear/python-twitter>`_.

Thanks a lot for Python-Twitter Developers.

============
Introduction
============

Library provides an easy way to use YouTube Data API V3.

=============
Documentation
=============

You can view the latest ``python-youtube`` documentation at: https://sns-sdks.github.io/python-youtube/.

Also view the full ``YouTube DATA API`` docs at: https://developers.google.com/youtube/v3/docs/.

==========
Installing
==========

You can install this lib from PyPI:

.. code:: shell

    pip install --upgrade python-youtube
    # ✨🍰✨

=====
Using
=====

The API is exposed via the ``pyyoutube.Api`` class.

-----------
INSTANTIATE
-----------

There provide two method to create instance the ``pyyoutube.Api``.

You can just initialize with an api key:

.. code-block:: python

    >>> from pyyoutube import Api
    >>> api = Api(api_key="your api key")

If you want to get some authorization data. you need to initialize with an access token:

.. code-block:: python

    >>> from pyyoutube import Api
    >>> api = Api(access_token='your api key')

You can read the docs to see how to get an access token.

Or you can ask for user to do oauth flow:

.. code-block:: python

    >>> from pyyoutube import Api
    >>> api = Api(client_id="client key", client_secret="client secret")
    # Get authorization url
    >>> api.get_authorization_url()
    ('https://accounts.google.com/o/oauth2/v2/auth?response_type=code&client_id=id&redirect_uri=https%3A%2F%2Flocalhost%2F&scope=scope&state=PyYouTube&access_type=offline&prompt=select_account', 'PyYouTube')
    # user to do
    # copy the response url
    >>> api.generate_access_token(authorization_response="link for response")
    AccessToken(access_token='token', expires_in=3599, token_type='Bearer')

Now you can use the instance to get data from YouTube.

------------
CHANNEL DATA
------------

The library provides several ways to get channel's data.

If a channel is not found, the property ``items`` will return with blank list.

You can use channel id:

.. code-block:: python

    >>> channel_by_id = api.get_channel_info(channel_id="UC_x5XG1OV2P6uZZ5FSM9Ttw")
    >>> channel_by_id.items
    [Channel(kind='youtube#channel', id='UC_x5XG1OV2P6uZZ5FSM9Ttw')]
    >>> channel_by_id.items[0].to_dict()
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

You can pass a channel id with comma-separated id string or a list, tuple or set of ids to get multiple channels.
Many methods also provide this functionality.

with ids:

.. code-block:: python

    >>> channel_by_ids = api.get_channel_info(channel_id="UC_x5XG1OV2P6uZZ5FSM9Ttw,UCa-vrCLQHviTOVnEKDOdetQ")
    >>> channel_by_ids.items
    [Channel(kind='youtube#channel', id='UC_x5XG1OV2P6uZZ5FSM9Ttw'),
     Channel(kind='youtube#channel', id='UCa-vrCLQHviTOVnEKDOdetQ')]

You can also use channel name:

.. code-block:: python

    >>> channel_by_username = api.get_channel_info(for_username="GoogleDevelopers")
    >>> channel_by_username.items[0]
    Channel(kind='youtube#channel', id='UC_x5XG1OV2P6uZZ5FSM9Ttw')

If you have authorized, you can get your channels:

.. code-block:: python

    >>> channel_by_mine = api_with_authorization.get_channel_info(mine=True)
    >>> channel_by_mine.items[0]
    Channel(kind='youtube#channel', id='UCa-vrCLQHviTOVnEKDOdetQ')

.. note::
    To get your channel, you must do authorization first, otherwise you will get an error.

--------
PLAYLIST
--------

There are methods to get playlists by playlist id, channel id or get your own playlists.

Get playlists by id:

.. code-block:: python

    >>> playlists_by_id = api.get_playlist_by_id(playlist_id="PLOU2XLYxmsIKpaV8h0AGE05so0fAwwfTw")
    >>> playlists_by_id.items
    [Playlist(kind='youtube#playlist', id='PLOU2XLYxmsIKpaV8h0AGE05so0fAwwfTw')]

Get playlists by channel (If you want to get all of atarget channel's playlists, just provide the parameter ``count=None``):

.. code-block:: python

    >>> playlists_by_channel = api.get_playlists(channel_id="UC_x5XG1OV2P6uZZ5FSM9Ttw")
    >>> playlists_by_channel.items
    [Playlist(kind='youtube#playlist', id='PLOU2XLYxmsIKpaV8h0AGE05so0fAwwfTw'),
     Playlist(kind='youtube#playlist', id='PLOU2XLYxmsIJO83u2UmyC8ud41AvUnhgj'),
     Playlist(kind='youtube#playlist', id='PLOU2XLYxmsILfV1LiUhDjbh1jkFjQWrYB'),
     Playlist(kind='youtube#playlist', id='PLOU2XLYxmsIKNr3Wfhm8o0TSojW7hEPPY'),
     Playlist(kind='youtube#playlist', id='PLOU2XLYxmsIJ8ItHmK4bRlY4GCzMgXLAJ')]

Get your playlists(this requires authorization):

.. code:: python

    playlists_by_mine = api.get_playlists(mine=True)

-------------
PLAYLIST ITEM
-------------

Similarly, you can get playlist items by playlist item id or playlist id.

Get playlist items by id:

.. code-block:: python

    >>> playlist_item_by_id = api.get_playlist_item_by_id(playlist_item_id="UExPVTJYTFl4bXNJS3BhVjhoMEFHRTA"
    ...     "1c28wZkF3d2ZUdy41NkI0NEY2RDEwNTU3Q0M2")

    >>> playlist_item_by_id.items
    [PlaylistItem(kind='youtube#playlistItem', id='UExPVTJYTFl4bXNJS3BhVjhoMEFHRTA1c28wZkF3d2ZUdy41NkI0NEY2RDEwNTU3Q0M2')]


Get playlist items by playlist id (If you want to get target playlist all items, just provide the parameter ``count=None``):

.. code-block:: python

    >>> playlist_item_by_playlist = api.get_playlist_items(playlist_id="PLOU2XLYxmsIKpaV8h0AGE05so0fAwwfTw", count=2)

    >>> playlist_item_by_playlist.items
    [PlaylistItem(kind='youtube#playlistItem', id='UExPVTJYTFl4bXNJS3BhVjhoMEFHRTA1c28wZkF3d2ZUdy41NkI0NEY2RDEwNTU3Q0M2'),
     PlaylistItem(kind='youtube#playlistItem', id='UExPVTJYTFl4bXNJS3BhVjhoMEFHRTA1c28wZkF3d2ZUdy4yODlGNEE0NkRGMEEzMEQy')]
    >>> playlist_item_by_id.items[0].snippet.resourceId
    ResourceId(kind='youtube#video', videoId='CvTApw9X8aA')

-----
VIDEO
-----

You can get a video's information by several methods.

Get videos by video id(s):

.. code-block:: python

    >>> video_by_id = api.get_video_by_id(video_id="CvTApw9X8aA")

    >>> video_by_id
    VideoListResponse(kind='youtube#videoListResponse')

    >>> video_by_id.items
    [Video(kind='youtube#video', id='CvTApw9X8aA')]


Get videos by chart (If you want to get all videos, just provide the parameter ``count=None``):

.. code-block:: python

    >>> video_by_chart = api.get_videos_by_chart(chart="mostPopular", region_code="US", count=2)

    >>> video_by_chart.items
    [Video(kind='youtube#video', id='RwnN2FVaHmw'),
     Video(kind='youtube#video', id='hDeuSfo_Ys0')]


Get videos by your rating (this requires authorization, also if you want to get all videos, just provide the parameter ``count=None``):

.. code:: python

    videos_by_rating = api.get_videos_by_myrating(rating="like", count=2)

--------------
COMMENT THREAD
--------------

You can get comment thread information by id or some filter.

Get comment thread by id(s):

.. code-block:: python

    >>> ct_by_id = api.get_comment_thread_by_id(comment_thread_id='Ugz097FRhsQy5CVhAjp4AaABAg,UgzhytyP79_Pwa
    ... Dd4UB4AaABAg')

    >>> ct_by_id.items
    [CommentThread(kind='youtube#commentThread', id='Ugz097FRhsQy5CVhAjp4AaABAg'),
     CommentThread(kind='youtube#commentThread', id='UgzhytyP79_PwaDd4UB4AaABAg')]

Get all comment threads related to a channel (including comment threads for the channel's video, also if you want to get all comment threads, just provide the parameter ``count=None``):

.. code-block:: python

    >>> ct_by_all = api.get_comment_threads(all_to_channel_id="UC_x5XG1OV2P6uZZ5FSM9Ttw", count=2)

    >>> ct_by_all.items
    [CommentThread(kind='youtube#commentThread', id='UgwlB_Cza9WtzUWahYN4AaABAg'),
     CommentThread(kind='youtube#commentThread', id='UgyvoQJ2LsxCBwGEpMB4AaABAg')]

Get comment threads only for the channel (If you want to get all comment threads, just provide the parameter ``count=None``):

.. code-block:: python

    >>> ct_by_channel = api.get_comment_threads(channel_id="UC_x5XG1OV2P6uZZ5FSM9Ttw", count=2)

    >>> ct_by_channel.items
    [CommentThread(kind='youtube#commentThread', id='UgyUBI0HsgL9emxcZpR4AaABAg'),
     CommentThread(kind='youtube#commentThread', id='Ugzi3lkqDPfIOirGFLh4AaABAg')]

Get comment threads only for the video (If you want to get all comment threads, just provide the parameter ``count=None``):

.. code-block:: python

    >>> ct_by_video = api.get_comment_threads(video_id="D-lhorsDlUQ", count=2)

    >>> ct_by_video.items
    [CommentThread(kind='youtube#commentThread', id='UgydxWWoeA7F1OdqypJ4AaABAg'),
     CommentThread(kind='youtube#commentThread', id='UgxKREWxIgDrw8w2e_Z4AaABAg')]

-------
COMMENT
-------

You can get comment information by id or use the top-level comment id to get replies.

.. note::
    The reply has the same structure as a comment.

Get comments by id(s):

.. code-block:: python

    >>> comment_by_id = api.get_comment_by_id(comment_id='UgxKREWxIgDrw8w2e_Z4AaABAg,UgyrVQaFfEdvaSzstj14Aa
    ... ABAg')

    >>> comment_by_id.items
    [Comment(kind='youtube#comment', id='UgxKREWxIgDrw8w2e_Z4AaABAg', snippet=CommentSnippet(authorDisplayName='Hieu Nguyen', likeCount=0)),
     Comment(kind='youtube#comment', id='UgyrVQaFfEdvaSzstj14AaABAg', snippet=CommentSnippet(authorDisplayName='Mani Kanta', likeCount=0))]

Get replies by comment id (If you want to get all comments, just provide the parameter ``count=None``):

.. code-block:: python

    >>> comment_by_parent = api.get_comments(parent_id="UgwYjZXfNCUTKPq9CZp4AaABAg")

    >>> comment_by_parent.items
    [Comment(kind='youtube#comment', id='UgwYjZXfNCUTKPq9CZp4AaABAg.8yxhlQJogG18yz_cXK9Kcj', snippet=CommentSnippet(authorDisplayName='Marlon López', likeCount=0))]

--------------
VIDEO CATEGORY
--------------

You can get video category with id or region.

Get video categories with id(s):

.. code-block:: python

    >>> video_category_by_id = api.get_video_categories(category_id="17,18")

    >>> video_category_by_id.items
    [VideoCategory(kind='youtube#videoCategory', id='17'),
     VideoCategory(kind='youtube#videoCategory', id='18')]

Get video categories with region code:

.. code-block:: python

    >>> video_categories_by_region = api.get_video_categories(region_code="US")

    >>> video_categories_by_region.items
    [VideoCategory(kind='youtube#videoCategory', id='1'),
     VideoCategory(kind='youtube#videoCategory', id='2'),
     VideoCategory(kind='youtube#videoCategory', id='10'),
     VideoCategory(kind='youtube#videoCategory', id='15'),
     ...]

-------------
SUBSCRIPTIONS
-------------

You can get subscription information by id, by point channel, or your own.

.. note::
    If you want to get the subscriptions not set to public, you need do authorization first and get the access token.
    You can see the demo `A demo for get my subscription <examples/subscription.py>`_.

To get subscription info by id(s), this needs your token to have the permission for the subscriptions belonging to a channel or user:

.. code-block:: python

    >>> r = api.get_subscription_by_id(
    ...         subscription_id=[
    ...             "zqShTXi-2-Tx7TtwQqhCBwViE_j9IEgnmRmPnqJljxo",
    ...             "zqShTXi-2-Rya5uUxEp3ZsPI3fZrFQnSXNQCwvHBGGo"])
    >>> r
    SubscriptionListResponse(kind='youtube#subscriptionListResponse')
    >>> r.items
    [Subscription(kind='youtube#subscription', id='zqShTXi-2-Tx7TtwQqhCBwViE_j9IEgnmRmPnqJljxo', snippet=SubscriptionSnippet(title='PyCon 2015', description='')),
     Subscription(kind='youtube#subscription', id='zqShTXi-2-Rya5uUxEp3ZsPI3fZrFQnSXNQCwvHBGGo', snippet=SubscriptionSnippet(title='ikaros-life', description='This is a test channel.'))]

Get your own subscriptions, this need you do authorization first or give the authorized access token:

.. code-block:: python

    >>> r = api.get_subscription_by_me(
    ...         mine=True,
    ...         parts=["id", "snippet"],
    ...         count=2
    ... )
    >>> r
    SubscriptionListResponse(kind='youtube#subscriptionListResponse')
    >>> r.items
    [Subscription(kind='youtube#subscription', id='zqShTXi-2-Tx7TtwQqhCBwtJ-Aho6DZeutqZiP4Q79Q', snippet=SubscriptionSnippet(title='Next Day Video', description='')),
     Subscription(kind='youtube#subscription', id='zqShTXi-2-Tx7TtwQqhCBwViE_j9IEgnmRmPnqJljxo', snippet=SubscriptionSnippet(title='PyCon 2015', description=''))]

Get public channel's subscriptions:

.. code-block:: python

    >>> r = api.get_subscription_by_channel(
    ...      channel_id="UCAuUUnT6oDeKwE6v1NGQxug",
    ...      parts="id,snippet",
    ...      count=2
    ... )
    >>> r
    SubscriptionListResponse(kind='youtube#subscriptionListResponse')
    >>> r.items
    [Subscription(kind='youtube#subscription', id='FMP3Mleijt-52zZDGkHtR5KhwkvCcdQKWWWIA1j5eGc', snippet=SubscriptionSnippet(title='TEDx Talks', description="TEDx is an international community that organizes TED-style events anywhere and everywhere -- celebrating locally-driven ideas and elevating them to a global stage. TEDx events are produced independently of TED conferences, each event curates speakers on their own, but based on TED's format and rules.\n\nFor more information on using TED for commercial purposes (e.g. employee learning, in a film, or in an online course), please submit a media request using the link below.")),
     Subscription(kind='youtube#subscription', id='FMP3Mleijt_ZKvy5M-HhRlsqI4wXY7VmP5g8lvmRhVU', snippet=SubscriptionSnippet(title='TED Residency', description='The TED Residency program is an incubator for breakthrough ideas. It is free and open to all via a semi-annual competitive application. Those chosen as TED Residents spend four months at TED headquarters in New York City, working on their idea. Selection criteria include the strength of their idea, their character, and their ability to bring a fresh perspective and positive contribution to the diverse TED community.'))]


----------
ACTIVITIES
----------

You can get activities by channel id. You can also get your own activities after you have completed authorization.

Get public channel activities:

.. code-block:: python

    >>> r = api.get_activities_by_channel(channel_id="UC_x5XG1OV2P6uZZ5FSM9Ttw", count=2)
    >>> r
    ActivityListResponse(kind='youtube#activityListResponse')
    >>> r.items
    [Activity(kind='youtube#activity', id='MTUxNTc3NzM2MDAyODIxOTQxNDM0NjAwMA==', snippet=ActivitySnippet(title='2019 Year in Review - The Developer Show', description='Here to bring you the latest developer news from across Google this year is Developer Advocate Timothy Jordan. In this last week of the year, we’re taking a look back at some of the coolest and biggest announcements we covered in 2019! \n\nFollow Google Developers on Instagram → https://goo.gle/googledevs\n\nWatch more #DevShow → https://goo.gle/GDevShow\nSubscribe to Google Developers → https://goo.gle/developers')),
     Activity(kind='youtube#activity', id='MTUxNTc3MTI4NzIzODIxOTQxNDM0NzI4MA==', snippet=ActivitySnippet(title='GDE Promo - Lara Martin', description='Meet Lara Martin, a Flutter/Dart Google Developers Expert and get inspired by her journey. Watch now for a preview of her story! #GDESpotlights #IncludedWithGoogle\n\nLearn about the GDE program → https://goo.gle/2qWOvAy\n\nGoogle Developers Experts → https://goo.gle/GDE\nSubscribe to Google Developers → https://goo.gle/developers'))]


Get your activities:

.. code-block:: python

    >>> r = api_with_token.get_activities_by_me()
    >>> r.items
    [Activity(kind='youtube#activity', id='MTUxNTc0OTk2MjI3NDE0MjYwMDY1NjAwODA=', snippet=ActivitySnippet(title='华山日出', description='冷冷的山头')),
     Activity(kind='youtube#activity', id='MTUxNTc0OTk1OTAyNDE0MjYwMDY1NTc2NDg=', snippet=ActivitySnippet(title='海上日出', description='美美美'))]

Get your video captions:

.. code-block:: python

    >>> r = api.get_captions_by_video(video_id="oHR3wURdJ94", parts=["id", "snippet"])
    >>> r
    CaptionListResponse(kind='youtube#captionListResponse')
    >>> r.items
    [Caption(kind='youtube#caption', id='SwPOvp0r7kd9ttt_XhcHdZthMwXG7Z0I', snippet=CaptionSnippet(videoId='oHR3wURdJ94', lastUpdated='2020-01-14T09:40:49.981Z')),
     Caption(kind='youtube#caption', id='fPMuDm722CIRcUAT3NTPQHQZJZJxt39kU7JvrHk8Kzs=', snippet=CaptionSnippet(videoId='oHR3wURdJ94', lastUpdated='2020-01-14T09:39:46.991Z'))]


If you already have caption id(s), you can get video caption by id(s):

.. code-block:: python

    >>> r = api.get_captions_by_video(video_id="oHR3wURdJ94", parts=["id", "snippet"], caption_id="SwPOvp0r7kd9ttt_XhcHdZthMwXG7Z0I")
    >>> r
    CaptionListResponse(kind='youtube#captionListResponse')
    >>> r.items
    [Caption(kind='youtube#caption', id='SwPOvp0r7kd9ttt_XhcHdZthMwXG7Z0I', snippet=CaptionSnippet(videoId='oHR3wURdJ94', lastUpdated='2020-01-14T09:40:49.981Z'))]

----------------
CHANNEL SECTIONS
----------------

You can get channel sections by self id or belonged channel id or your own channel.

Get channel sections by channel id:

.. code-block:: python

    >>> r = api.get_channel_sections_by_channel(channel_id="UC_x5XG1OV2P6uZZ5FSM9Ttw")
    >>>> r
    ChannelSectionResponse(kind='youtube#channelSectionListResponse')
    >>> r.items
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

Get authorized user's channel sections:

.. code-block:: python

    >>> r = api.get_channel_sections_by_channel(mine=True)
    >>> r.items
    [ChannelSection(kind='youtube#channelSection', id='UCa-vrCLQHviTOVnEKDOdetQ.jNQXAC9IVRw'),
     ChannelSection(kind='youtube#channelSection', id='UCa-vrCLQHviTOVnEKDOdetQ.LeAltgu_pbM'),
     ChannelSection(kind='youtube#channelSection', id='UCa-vrCLQHviTOVnEKDOdetQ.nGzAI5pLbMY')]

Get channel section detail info by id:

.. code-block:: python

    >>> r = api.get_channel_section_by_id(section_id="UC_x5XG1OV2P6uZZ5FSM9Ttw.e-Fk7vMPqLE")
    >>> r
    ChannelSectionResponse(kind='youtube#channelSectionListResponse')
    >>> r1.items
    [ChannelSection(kind='youtube#channelSection', id='UC_x5XG1OV2P6uZZ5FSM9Ttw.e-Fk7vMPqLE')]

-------------
I18N RESOURCE
-------------

You can get a list of content regions that the YouTube website supports:

.. code-block:: python

    >>> r = api.get_i18n_regions(parts=["snippet"])
    >>> r.items
    [I18nRegion(kind='youtube#i18nRegion', id='DZ', snippet=I18nRegionSnippet(gl='DZ', name='Algeria')),
     I18nRegion(kind='youtube#i18nRegion', id='AR', snippet=I18nRegionSnippet(gl='AR', name='Argentina')),
     I18nRegion(kind='youtube#i18nRegion', id='AU', snippet=I18nRegionSnippet(gl='AU', name='Australia'))
     ...]

You can get a list of application languages that the YouTube website supports:

.. code-block:: python

    >>> r = api.get_i18n_languages(parts=["snippet"])
    >>> r.items
    [I18nLanguage(kind='youtube#i18nLanguage', id='af', snippet=I18nLanguageSnippet(hl='af', name='Afrikaans')),
     I18nLanguage(kind='youtube#i18nLanguage', id='az', snippet=I18nLanguageSnippet(hl='az', name='Azerbaijani')),
     I18nLanguage(kind='youtube#i18nLanguage', id='id', snippet=I18nLanguageSnippet(hl='id', name='Indonesian')),
     ...]


-------
MEMBER
-------

The API request must be authorized by the channel owner.

You can retrieve a list of members (formerly known as "sponsors") for a channel:

.. code-block:: python

    >>> r = api_with_token.get_members(parts=["snippet"])
    >>> r.items
    [MemberListResponse(kind='youtube#memberListResponse'),
     MemberListResponse(kind='youtube#memberListResponse')]


----------------
MEMBERSHIP LEVEL
----------------

The API request must be authorized by the channel owner.

You can retrieve a list membership levels for a channel:

.. code-block:: python

    >>> r = api_with_token.get_membership_levels(parts=["snippet"])
    >>> r.items
    [MembershipsLevelListResponse(kind='youtube#membershipsLevelListResponse'),
     MembershipsLevelListResponse(kind='youtube#membershipsLevelListResponse')]


-------------------------
VIDEO ABUSE REPORT REASON
-------------------------

You can retrieve a list of reasons that can be used to report abusive videos:

.. code-block:: python

    >>> r = api_with_token.get_video_abuse_report_reason(parts=["snippet"])
    >>> r.items
    [VideoAbuseReportReason(kind='youtube#videoAbuseReportReason'),
     VideoAbuseReportReason(kind='youtube#videoAbuseReportReason')]

------
SEARCH
------

You can use those methods to search the video,playlist,channel data. For more info, you can see the `Search Request Docs <https://developers.google.com/youtube/v3/docs/search/list>`_ .

You can search different type of resource with keywords:

.. code-block:: python

    >>> r = api.search_by_keywords(q="surfing", search_type=["channel","video", "playlist"], count=5, limit=5)
    >>> r.items
    [SearchResult(kind='youtube#searchResult'),
     SearchResult(kind='youtube#searchResult'),
     SearchResult(kind='youtube#searchResult'),
     SearchResult(kind='youtube#searchResult'),
     SearchResult(kind='youtube#searchResult')]

You can search your app send videos:

.. code-block:: python

    >>> r = api_with_token.search_by_developer(q="news", count=1)
    >>> r.items
    [SearchResult(kind='youtube#searchResult')]

You can search your videos:

.. code-block:: python

    >>> r = api_with_token.search_by_mine(q="news", count=1)
    >>> r.items
    [SearchResult(kind='youtube#searchResult')]

Or you can build your request using the ``search`` method:

.. code-block:: python

    >>> r = api.search(
    ...     location="21.5922529, -158.1147114",
    ...     location_radius="10mi",
    ...     q="surfing",
    ...     parts=["snippet"],
    ...     count=5,
    ...     published_after="2020-02-01T00:00:00Z",
    ...     published_before="2020-03-01T00:00:00Z",
    ...     safe_search="moderate",
    ...     search_type="video")
    >>> r.items
    [SearchResult(kind='youtube#searchResult'),
     SearchResult(kind='youtube#searchResult'),
     SearchResult(kind='youtube#searchResult'),
     SearchResult(kind='youtube#searchResult'),
     SearchResult(kind='youtube#searchResult')]

    >>> r = api.search(
    ...     event_type="live",
    ...     q="news",
    ...     count=3,
    ...     parts=["snippet"],
    ...     search_type="video",
    ...     topic_id="/m/09s1f",
    ...     order="viewCount")
    >>> r.items
    [SearchResult(kind='youtube#searchResult'),
     SearchResult(kind='youtube#searchResult'),
     SearchResult(kind='youtube#searchResult')]

====
TODO
====

The following apis are now available:

- OAuth Flow
- Channel Info
- Playlist Info
- PlaylistItem Info
- Video Info
- Comment Thread Info
- Comment Info
- Video Categories Info
- Subscriptions Info
- Activities Info
- Captions Info
- Channel Sections Info
- Search Requests and simple usage.
- Members Info
- Membership Level Info

Doing

- Update, Insert and so on.
