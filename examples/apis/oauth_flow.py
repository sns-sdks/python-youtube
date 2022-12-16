"""
    This example demonstrates how to perform authorization.
"""

from pyyoutube import Api

CLIENT_ID = "xxx"  # Your app id
CLIENT_SECRET = "xxx"  # Your app secret
SCOPE = [
    "https://www.googleapis.com/auth/youtube",
    "https://www.googleapis.com/auth/youtube.force-ssl",
    "https://www.googleapis.com/auth/userinfo.profile",
]


def do_authorize():
    api = Api(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)

    authorize_url, state = api.get_authorization_url(scope=SCOPE)
    print(f"Click url to do authorize: {authorize_url}")

    response_uri = input("Input youtube redirect uri:\n")

    token = api.generate_access_token(authorization_response=response_uri, scope=SCOPE)
    print(f"Your token: {token}")

    # get data
    profile = api.get_profile()
    print(f"Your channel id: {profile.id}")


if __name__ == "__main__":
    do_authorize()
