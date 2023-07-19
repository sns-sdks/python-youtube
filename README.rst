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

.. 

    Recently, we are working on the new structure for the library. `Read docs <docs/docs/introduce-new-structure.md>`_ to get more detail.

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

Now, the library covers all resource methods, including ``insert``,``update`` and so on.

Currently, we recommend using ``pyyoutube.Client`` to operate DATA API. It has more features.

Work with Client
----------------

You can just initialize with an api key:

.. code-block:: python

    >>> from pyyoutube import Client
    >>> client = Client(api_key="your api key")

If you want to get some authorization data. you need to initialize with an access token:

.. code-block:: python

    >>> from pyyoutube import Client
    >>> client = Client(access_token='your access token')

You can read the docs to see how to get an access token.

Or you can ask for user to do oauth flow:

.. code-block:: python

    >>> from pyyoutube import Client
    >>> client = Client(client_id="client key", client_secret="client secret")

    >>> client.get_authorize_url()
    ('https://accounts.google.com/o/oauth2/v2/auth?response_type=code&client_id=id&redirect_uri=https%3A%2F%2Flocalhost%2F&scope=scope&state=PyYouTube&access_type=offline&prompt=select_account', 'PyYouTube')

    >>> client.generate_access_token(authorization_response="link for response")
    AccessToken(access_token='token', expires_in=3599, token_type='Bearer')

Now you can use the instance to get data from YouTube.

Get channel detail:

    >>> cli.channels.list(channel_id="UC_x5XG1OV2P6uZZ5FSM9Ttw")
    ChannelListResponse(kind='youtube#channelListResponse')
    >>> cli.channels.list(channel_id="UC_x5XG1OV2P6uZZ5FSM9Ttw", return_json=True)
    {'kind': 'youtube#channelListResponse',
     'etag': 'eHSYpB_FqHX8vJiGi_sLCu0jkmE',
    ...
    }

To get more usage to see our `client docs <docs/docs/usage/work-with-client.md>`_, or `client examples <examples/clients>`_

Work with API
----------------

..

    We still support the old way for the sake of compatibility with older users.

You can just initialize with an api key:

.. code-block:: python

    >>> from pyyoutube import Api
    >>> api = Api(api_key="your api key")

If you want to get some authorization data. you need to initialize with an access token:

.. code-block:: python

    >>> from pyyoutube import Api
    >>> api = Api(access_token='your access token')

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

Get channel detail:

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
      # Get json response from youtube
      >>> api.get_channel_info(channel_id="UC_x5XG1OV2P6uZZ5FSM9Ttw", return_json=True)
      {'kind': 'youtube#channelListResponse',
        'etag': '17FOkdjp-_FPTiIJXdawBS4jWtc',
        ...
       }

To get more usage to see our `api docs <docs/docs/usage/work-with-api.md>`_, or `api examples <examples/apis>`_
