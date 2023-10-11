"""
    This example demonstrates how to perform authorization.
"""

from pyyoutube import Client


CLIENT_ID = "xxx"  # Your app id
CLIENT_SECRET = "xxx"  # Your app secret
CLIENT_SECRET_PATH = None  # or your path/to/client_secret_web.json

SCOPE = [
    "https://www.googleapis.com/auth/youtube",
    "https://www.googleapis.com/auth/youtube.force-ssl",
    "https://www.googleapis.com/auth/userinfo.profile",
]


def do_authorize():
    cli = Client(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    # or if you want to use a web type client_secret.json
    # cli = Client(client_secret_path=CLIENT_SECRET_PATH)

    authorize_url, state = cli.get_authorize_url(scope=SCOPE)
    print(f"Click url to do authorize: {authorize_url}")

    response_uri = input("Input youtube redirect uri:\n")

    token = cli.generate_access_token(authorization_response=response_uri, scope=SCOPE)
    print(f"Your token: {token}")

    # get data
    resp = cli.channels.list(mine=True)
    print(f"Your channel id: {resp.items[0].id}")


if __name__ == "__main__":
    do_authorize()
