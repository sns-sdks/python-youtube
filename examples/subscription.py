"""
    This demo show how to use this library to do authorization and get your subscription.
"""

import pyyoutube
import webbrowser

CLIENT_ID = "your app id"
CLIENT_SECRET = "your app secret"


def get_subscriptions():
    api = pyyoutube.Api(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)

    # need follows scope
    scope = ["https://www.googleapis.com/auth/youtube.readonly"]

    url, _ = api.get_authorization_url(scope=scope)

    print(
        "Try to start a browser to visit the authorization page. If not opened. you can copy and visit by hand:\n"
        f"{url}"
    )
    webbrowser.open(url)

    auth_response = input(
        "\nCopy the whole url if you finished the step to authorize:\n"
    )

    api.exchange_code_to_access_token(authorization_response=auth_response)

    sub_res = api.get_subscription_by_me(mine=True, parts="id,snippet", count=None)

    with open("subscriptions.json", "w+") as f:
        f.write(sub_res.to_json())

    print("Finished.")


if __name__ == "__main__":
    get_subscriptions()
