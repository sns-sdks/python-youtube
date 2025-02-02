# Examples

We provide two entry points to operate the YouTube DATA API.

- Api `from pyyoutube import Api`: This is an old implementation used to be compatible with older versions of code.
- Client `from pyyoutube import Client`: This is a new implementation for operating the API and provides additional
  capabilities.

# Basic Usage

## API

```python
from pyyoutube import Api

api = Api(api_key="your key")
api.get_channel_info(channel_id="id for channel")
# ChannelListResponse(kind='youtube#channelListResponse')
```

You can get more examples at [api examples](/examples/apis/).

## Client

```python
from pyyoutube import Client

cli = Client(api_key="your key")
cli.channels.list(channel_id="UC_x5XG1OV2P6uZZ5FSM9Ttw")
# ChannelListResponse(kind='youtube#channelListResponse')
```

You can get more examples at [client examples](/examples/clients/).
