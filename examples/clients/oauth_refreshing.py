"""
    This example demonstrates how to automatically (re)generate tokens for continuous OAuth.
    We store the Access Token in a seperate .env file to be used later.
"""

from pyyoutube import Client
from json import loads, dumps
from pathlib import Path


CLIENT_ID = "xxx"  # Your app id
CLIENT_SECRET = "xxx"  # Your app secret
CLIENT_SECRET_PATH = None  # or your path/to/client_secret_web.json

TOKEN_PERSISTENT_PATH = None # path/to/persistent_token_storage_location

SCOPE = [
    "https://www.googleapis.com/auth/youtube",
    "https://www.googleapis.com/auth/youtube.force-ssl",
    "https://www.googleapis.com/auth/userinfo.profile",
]

def do_refresh():
    token_location = Path(TOKEN_PERSISTENT_PATH)

    # Read the persistent token data if it exists
    token_data = {}
    if token_location.exists():
        token_data = loads(token_location.read_text())
    

    cli = Client(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        access_token=token_data.get("access_token"),
        refresh_token=token_data.get("refresh_token")
    )
    # or if you want to use a web type client_secret.json
    # cli = Client(
    #     client_secret_path=CLIENT_SECRET_PATH,
    #     access_token=token_data.get("access_token"),
    #     refresh_token=token_data.get("refresh_token")
    # )

    # If no access token is provided, this is the same as oauth_flow.py
    if not cli._has_auth_credentials():
        authorize_url, state = cli.get_authorize_url(scope=SCOPE)
        print(f"Click url to do authorize: {authorize_url}")

        response_uri = input("Input youtube redirect uri:\n")

        token = cli.generate_access_token(authorization_response=response_uri, scope=SCOPE)
        print(f"Your token: {token}")

    # Otherwise, refresh the access token if it has expired
    else:
        token = cli.refresh_access_token(cli.refresh_token)

        # we add the token data to the client and token objects so that they are complete
        token.refresh_token = cli.refresh_token
        cli.access_token = token.access_token
        print(f"Your token: {token}")

    # Write the token data to the persistent location to be used again, ensuring the file exists
    token_location.mkdir(parents=True, exist_ok=True)
    token_location.write_text(
        dumps(
            {
                "access_token": token.access_token,
                "refresh_token": token.refresh_token
            }
        )
    )

    # Now you can do things with the client
    resp = cli.channels.list(mine=True)
    print(f"Your channel id: {resp.items[0].id}")

if __name__ == "__main__":
    do_refresh()
