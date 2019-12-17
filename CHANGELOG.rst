Changelog
---------

Version 0.5.1
=============

Now some apis can get all target items just by one method call.

For example, you can get playlist's all items by follow call::

    In [1]: r = api.get_playlist_items(playlist_id="PLWz5rJ2EKKc_xXXubDti2eRnIKU0p7wHd", parts=["id", "snippet"], count=None)
    In [2]: r.pageInfo
    Out[2]: PageInfo(totalResults=73, resultsPerPage=50)
    In [3]: len(r.items)
    Out[4]: 73

You can see the `README <https://github.com/sns-sdks/python-youtube/blob/master/README.rst>`_ to find which methods support this.

Version 0.5.0
=============

Broken Change
+++++++++++++

Now introduce new model ApiResponse representing the response from youtube, so previous usage has been invalidated.

You need to read the docs to get more change `Modules Documentation <https://python-youtube.readthedocs.io/en/latest/pyyoutube.html#module-pyyoutube.api>`_,
or see the `README <https://github.com/sns-sdks/python-youtube/blob/v0.5.0/README.rst>`_ to get the simple new usage.

What's New
++++++++++

Split some method into multiple usage, for example get video has been split three methods:

* api.get_video_by_id()
* api.get_videos_by_chart()
* api.get_videos_by_myrating()
