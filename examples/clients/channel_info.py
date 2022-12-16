"""
    This example demonstrates how to retrieve information for a channel.
"""

from pyyoutube import Client

API_KEY = "Your key"  # replace this with your api key.


def get_channel_info():
    cli = Client(api_key=API_KEY)

    channel_id = "UC_x5XG1OV2P6uZZ5FSM9Ttw"

    resp = cli.channels.list(
        channel_id=channel_id, parts=["id", "snippet", "statistics"], return_json=True
    )
    print(f"Channel info: {resp['items'][0]}")


if __name__ == "__main__":
    get_channel_info()
