Python YouTube

A Python wrapper around for YouTube Data API V3.

.. image:: https://travis-ci.org/MerleLiuKun/python-youtube.svg?branch=master
    :target: https://travis-ci.org/MerleLiuKun/python-youtube
    :alt: Build Status

======
THANKS
======

This project structure is base on `Python-Twitter <https://github.com/bear/python-twitter>`_.

Thanks a lot for Python-Twitter Developers.

============
Introduction
============

Library provides a service to easy use YouTube Data API V3.

The api docs you can find on `YouTube Data API Reference <https://developers.google.com/youtube/v3/docs/>`_

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

====
TODO
====

Now this has follows api.

- Channel Info
- Playlist Info
- PlaylistItem Info
- Video Info

Doing:

- comments