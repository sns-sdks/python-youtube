Python YouTube

A Python wrapper around for YouTube Data API V3.

.. image:: https://travis-ci.org/MerleLiuKun/python-youtube.svg?branch=master
    :target: https://travis-ci.org/MerleLiuKun/python-youtube

.. image:: https://readthedocs.org/projects/python-youtube/badge/?version=latest
    :target: https://python-youtube.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://codecov.io/gh/MerleLiuKun/python-youtube/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/MerleLiuKun/python-youtube

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

Library provides a service to easy use YouTube Data API V3.

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

To create an instance of the ``pyyoutube.Api`` with two different methods.
Use only api key or provide google client id and key.
Now only for api key::

    In [1]: from pyyoutube import Api
    In [2]: api = Api(api_key='your api key')


To fetch one youtube channel's data::

    In [3]: res = api.get_channel_info(channel_name='GoogleDevelopers')

    In [4]: res
    Out[5]: Channel(id=UC_x5XG1OV2P6uZZ5FSM9Ttw,kind=youtube#channel)

To fetch youtube channel's playlists::

    In [6]: res = api.get_playlist(channel_id='UC_x5XG1OV2P6uZZ5FSM9Ttw')

    In [7]: res
    Out[7]:
    ([Playlist(id=PLOU2XLYxmsIJpufeMHncnQvFOe0K3MhVp,kind=youtube#playlist),
      Playlist(id=PLOU2XLYxmsIJXsH2htG1g0NUjHGq62Q7i,kind=youtube#playlist),
      Playlist(id=PLOU2XLYxmsIJJVnHWmd1qfr0Caq4VZCu4,kind=youtube#playlist),
      Playlist(id=PLOU2XLYxmsIKW-llcbcFdpR9RjCfYHZaV,kind=youtube#playlist),
      Playlist(id=PLOU2XLYxmsIIOSO0eWuj-6yQmdakarUzN,kind=youtube#playlist)],
     {'totalResults': 416, 'resultsPerPage': 5})

To fetch one playlist's items::

    In [8]: res = api.get_playlist_item(playlist_id='PLOU2XLYxmsIJpufeMHncnQvFOe0K3MhVp')

    In [9]: res
    Out[9]:
    ([PlaylistItem(id=UExPVTJYTFl4bXNJSnB1ZmVNSG5jblF2Rk9lMEszTWhWcC41NkI0NEY2RDEwNTU3Q0M2,kind=youtube#playlistItem),
      PlaylistItem(id=UExPVTJYTFl4bXNJSnB1ZmVNSG5jblF2Rk9lMEszTWhWcC4yODlGNEE0NkRGMEEzMEQy,kind=youtube#playlistItem),
      PlaylistItem(id=UExPVTJYTFl4bXNJSnB1ZmVNSG5jblF2Rk9lMEszTWhWcC4wMTcyMDhGQUE4NTIzM0Y5,kind=youtube#playlistItem),
      PlaylistItem(id=UExPVTJYTFl4bXNJSnB1ZmVNSG5jblF2Rk9lMEszTWhWcC41MjE1MkI0OTQ2QzJGNzNG,kind=youtube#playlistItem)],
     {'totalResults': 4, 'resultsPerPage': 5})

    In [10]: res[0][1].snippet.resourceId
    Out[10]: {'kind': 'youtube#video', 'videoId': 'cxABjSOa6RY'}

To fetch one youtube video's data::

    In [11]: res = api.get_video_info(video_id='cxABjSOa6RY')

    In [12]: res
    Out[12]: Video(id=cxABjSOa6RY,kind=youtube#video)

To fetch many youtube video's data::

    In [13]: res = api.get_videos_info(video_ids=['cxABjSOa6RY', '21BbGGGrq9s'])

    In [14]: res
    Out[14]:
    [Video(id=cxABjSOa6RY,kind=youtube#video),
     Video(id=21BbGGGrq9s,kind=youtube#video)]

Fetch comment thread info. You can use multi different parameter.
If you want to get the channel and the channel's videos comment threads.
You can provide target channel id with `all_to_channel_id` parameter. Like follows::

    In [5]: resp = api.get_comment_threads(all_to_channel_id='UC_x5XG1OV2P6uZZ5FSM9Ttw', count=4)

    In [6]: resp
    Out[6]:
    [CommentTread(id=UgzhytyP79_PwaDd4UB4AaABAg,kind=youtube#commentThread),
     CommentTread(id=UgxE6j_nUNlYMy_zy7R4AaABAg,kind=youtube#commentThread),
     CommentTread(id=UgwpW-4vURZSRbawXft4AaABAg,kind=youtube#commentThread),
     CommentTread(id=UgxUFyEVxBbWSIr7zrN4AaABAg,kind=youtube#commentThread)]

If you want to just get a channel comment threads. use `channel_id` instead of `all_to_channel_id`. Like follows::

    In [7]: resp = api.get_comment_threads(channel_id='UC_x5XG1OV2P6uZZ5FSM9Ttw', count=4)

If you want to get a video comment threads. You can provide target video id with `video_id`. Like follows::

    In [7]: resp = api.get_comment_threads(video_id='D-lhorsDlUQ', count=2)

    In [8]: resp
    Out[8]:
    [CommentTread(id=UgydxWWoeA7F1OdqypJ4AaABAg,kind=youtube#commentThread),
     CommentTread(id=UgxKREWxIgDrw8w2e_Z4AaABAg,kind=youtube#commentThread)]

If you want get comment thread detail info. You can provide comment thread id or comma-separated id list. Like follows::

    In [8]: resp = api.get_comment_thread_info(comment_thread_id='Ugz097FRhsQy5CVhAjp4AaABAg,UgzhytyP79_PwaDd4UB4AaABAg')

    In [9]: resp
    Out[9]:
    [CommentTread(id=Ugz097FRhsQy5CVhAjp4AaABAg,kind=youtube#commentThread),
     CommentTread(id=UgzhytyP79_PwaDd4UB4AaABAg,kind=youtube#commentThread)]

Fetch comments info. You can use multi different parameter.
If you want to get top level's comment's replies. Like follows::

    In [10]: resp = api.get_comments_by_parent(parent_id='UgwYjZXfNCUTKPq9CZp4AaABAg')

    In [11]: resp
    Out[11]: [Comment(id=UgwYjZXfNCUTKPq9CZp4AaABAg.8yxhlQJogG18yz_cXK9Kcj,kind=youtube#comment)]

If want get comment detail info. You can provide comment id or comma-separated id list. Like follows::

    In [12]: resp = api.get_comment_info(comment_id='UgxKREWxIgDrw8w2e_Z4AaABAg,UgyrVQaFfEdvaSzstj14AaABAg')

    In [13]: resp
    Out[13]:
    [Comment(id=UgxKREWxIgDrw8w2e_Z4AaABAg,kind=youtube#comment),
     Comment(id=UgyrVQaFfEdvaSzstj14AaABAg,kind=youtube#comment)]

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

Doing

- Refactor API.