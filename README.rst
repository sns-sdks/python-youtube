Python YouTube

A Python wrapper around for YouTube Data API.

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

Library provides a service to easy use YouTube web api.

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

    In [3]: res = api.get_channel_info(channel_name='Nba')

    In [4]: res
    Out[5]: Channel(id=UCWJ2lWNubArHWmf3FIHbfcQ,kind=youtube#channel)


To fetch one youtube video's data::

    In [5]: res_v = api.get_video_info(video_id='Ks-_Mh1QhMc')

    In [6]: res_v
    Out[6]: Video(id=Ks-_Mh1QhMc,kind=youtube#video)

To fetch many youtube video's data::

    In [7]: res = api.get_videos_info(video_ids=['c0KYU2j0TM4', 'eIho2S0ZahI'])

    In [8]: res
    Out[8]:
    [Video(id=c0KYU2j0TM4,kind=youtube#video),
     Video(id=eIho2S0ZahI,kind=youtube#video)]

====
TODO
====

on going
