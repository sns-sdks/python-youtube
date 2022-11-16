This doc will show you the new api structure for this library.

## Brief

To make the package easier to maintain and easy to use. We are shifted to using classes for different YouTube resources in an easier, higher-level programming experience.

![structure-uml](images/structure-uml.png)


In this structure, every resource will have self class. And to operate with YouTube API.

## Simple usage


### Initial Client

```python
from pyyoutube import Client

client = Client(api_key="your api key")
```

### Get data.

for example to get channel data.

```python
resp = client.channels.list(
    parts=["id", "snippet"],
    channel_id="UCa-vrCLQHviTOVnEKDOdetQ"    
)
# resp output
# ChannelListResponse(kind='youtube#channelListResponse')
# resp.items[0].id  output
# UCa-vrCLQHviTOVnEKDOdetQ
```
