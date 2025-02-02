If you want to get more data for your channel, You need provide the authorization.

This doc shows how to authorize a client.

## Prerequisite

To begin with, you must know what authorization is.

You can see some information at the [Official Documentation](https://developers.google.com/youtube/v3/guides/authentication).

You will need to create an app with [Access scope](https://developers.google.com/youtube/v3/guides/auth/server-side-web-apps#identify-access-scopes) approval by YouTube.

Once complete, you will be able to do a simple authorize with `Python-Youtube` library.

## Get authorization url

Suppose now we want to get user's permission to manage their YouTube account.

For the `Python-YouTube` library, the default scopes are:

- https://www.googleapis.com/auth/youtube
- https://www.googleapis.com/auth/userinfo.profile

You can get more scope information at [Access scopes](https://developers.google.com/youtube/v3/guides/auth/server-side-web-apps#identify-access-scopes).

(The defailt redirect URI used in PyYoutube is `https://localhost/`)

We can now perform the following steps:

Initialize the api instance with your app credentials

```
In [1]: from pyyoutube import Client

In [2]: cli = Client(client_id="you client id", client_secret="you client secret")

In [3]: cli.get_authorize_url()
Out[3]:
('https://accounts.google.com/o/oauth2/v2/auth?response_type=code&client_id=client_id&redirect_uri=https%3A%2F%2Flocalhost%2F&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fyoutube+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.profile&state=PyYouTube&access_type=offline&prompt=select_account',
 'PyYouTube')
```

Open your broswer of choice and copy the link returned by `get_authorize_url()` into the searchbar.

## Do authorization

On entering the URL, you will see the following:

![auth-1-chose-account](images/auth-1-chose-account.png)

Select the account to authorize your app to read data from.

If your app is not approved for use, you will recieve a warning. You can prevent this by adding your chosen Google account as a test member on your created OAuth application.
Otherwise, you will see the following:

![auth-2-not-approval](images/auth-2-not-approval.png)

You will need to click ``Advanced``, then click the ``Go to Python-YouTube (unsafe)``.

![auth-3-advanced](images/auth-3-advanced.png)

You should now see a window to select permissions granted to the application.

![auth-4-allow-permission](images/auth-4-allow-permission.png)

Click `allow` to give the permission.

You will see a Connection Error, as the link is redirecting to `localhost`. This is standard behaviour, so don't close the window or return to a previous page!

## Retrieve access token

Copy the full redicted URL from the browser address bar, and return to your original console.

```
In [4]: token = cli.generate_access_token(authorization_response="$redirect_url")

In [5]: token
Out[5]: AccessToken(access_token='access token', expires_in=3600, token_type='Bearer')
```
    
(Replace `$redirect_url` with the URL you copied)

You now have an access token to view your account data.


## Get your data

For example, you can get your playlists.

```
In [6]: playlists = cli.playlists.list(mine=True)

In [7]: playlists.items
Out[7]:
[Playlist(kind='youtube#playlist', id='PLBaidt0ilCManGDIKr8UVBFZwN_UvMKvS'),
 Playlist(kind='youtube#playlist', id='PLBaidt0ilCMbUdj0EppB710c_X5OuCP2g')]
```

!!! note "Tips"

    If you are confused, it is beneficial to read the [Authorize Requests](https://developers.google.com/youtube/v3/guides/authentication) guide first.
