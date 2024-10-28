# Changelog

All notable changes to this project will be documented in this file.

## Version 0.9.7 (2024-10-28)

### What's New

- Fix dependencies.

## Version 0.9.6 (2024-09-09)

### What's New

-Add new part field `recordingDetails` for video resource. Thanks for [@vmx](https://github.com/vmx)

## Version 0.9.5 (2024-08-09)

### What's New

- Make video regionRestriction fields to Optional. Thanks for [@pidi3000](https://github.com/pidi3000)
- Modify some examples. Thanks for [@pidi3000](https://github.com/pidi3000)
- fix enf_parts for part with whitespaces. Thanks for [@pidi3000](https://github.com/pidi3000)

## Version 0.9.4 (2024-02-18)

### What's New

- Add new parameter `for_handle` to get channel by handle.  
- fix some wrong error message.

## Version 0.9.3 (2023-11-22)

### What's New

- Add initial client with client_secret file. Thanks for [@pidi3000](https://github.com/pidi3000)

## Version 0.9.2 (2023-09-26)

### What's New

- Add new parameter for search method
- Mark some parameter or method to be deprecated.

## Version 0.9.1 (2023-07-19)

### What's New

- upgrade poetry. Thanks for [@blaggacao](https://github.com/blaggacao)

## Version 0.9.0 (2022-12-26)

### What's New

- Introduce new `Client` to operate YouTube DATA API. [#120](https://github.com/sns-sdks/python-youtube/issues/120).
- More example to show library usage.

## Version 0.8.3 (2022-10-17)

### What's New

- Add parts for video, thanks for [@Omer](https://github.com/dusking)

## Version 0.8.2 (2022-03-16)

### What's New

- Update OAuthorize functions.
- Update for examples.

## Version 0.8.1 (2021-05-14)

### Deprecation

Detail at: https://developers.google.com/youtube/v3/revision_history#may-12,-2021

- Remove channel resource in brandingSettings for channel.
- Remove localizations,targeting resource and some snippet resource for channelSection.
- Remove tags in snippet for playlist. 

### Broken Change

Methods `get_channel_sections_by_channel`, `get_channel_section_by_id` has remove parameter `hl`.


## Version 0.8.0

### Broken Change

Modify the auth flow methods.

### What's New

1. add python3.9 tests
2. New docs


## Version 0.7.0

### What's New

1. Add api methods for members and membership levels
2. Add more examples for api
3. Add fields for playlist item api
4. fix some.


## Version 0.6.1

### What's New

Remove deprecated api.


## Version 0.6.0

### What's New

Provide remain get apis. like activities, captions, channel_sections, i18n, video_abuse_report_reason, search resource and so on.

You can see the `README`_ to get more detail for those api.


## Version 0.5.3

### What's New

Provide the page token parameter to skip data have retrieved.

This for follow api methods

```python
api.get_playlists()
api.get_playlist_items()
api.get_videos_by_chart()
api.get_videos_by_myrating()
api.get_comment_threads()
api.get_comments()
api.get_subscription_by_channel()
api.get_subscription_by_me()
```

example

```
In[1]: r = api.get_subscription_by_channel(channel_id="UCAuUUnT6oDeKwE6v1NGQxug", limit=5, count=None, page_token="CAUQAA")
In[2]:r.prevPageToken
Out[2]: 'CAUQAQ'
```


## Version 0.5.2

### What's New

Now you can use authorized access token to get your subscriptions.
You can to the demo [A demo for get my subscription](https://github.com/sns-sdks/python-youtube/blob/master/examples/subscription.py) to see simple usage.
Or you can see the [subscriptions usage](https://github.com/sns-sdks/python-youtube/blob/master/README.rst#subscriptions) docs.

    #43 add api for get my subscriptions

    #41 add api for channel subscriptions



## Version 0.5.1

### What's New

Now some apis can get all target items just by one method call.

For example, you can get playlist's all items by follow call

```
In [1]: r = api.get_playlist_items(playlist_id="PLWz5rJ2EKKc_xXXubDti2eRnIKU0p7wHd", parts=["id", "snippet"], count=None)
In [2]: r.pageInfo
Out[2]: PageInfo(totalResults=73, resultsPerPage=50)
In [3]: len(r.items)
Out[4]: 73
```

You can see the [README](https://github.com/sns-sdks/python-youtube/blob/master/README.rst) to find which methods support this.

## Version 0.5.0

### **Broken Change**

Now introduce new model ApiResponse representing the response from youtube, so previous usage has been invalidated.

You need to read the docs [README](https://github.com/sns-sdks/python-youtube/blob/master/README.rst) to get the simple new usage.

### What's New

Split some method into multiple usage, for example get video has been split three methods:

* api.get_video_by_id()
* api.get_videos_by_chart()
* api.get_videos_by_myrating()
