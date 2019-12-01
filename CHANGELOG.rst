Changelog
---------

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
