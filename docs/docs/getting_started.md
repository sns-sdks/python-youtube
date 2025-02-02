This document is a simple tutorial to show how to use this library to get data from YouTube data API.

You can get the whole description for the YouTube API at [YouTube API Reference](https://developers.google.com/youtube/v3/docs/).

## Prerequisite

To begin, you need to create a [Google Project](https://console.cloud.google.com) with your google account.

Every new account has a free quota of 12 projects.

## Create your project

Click `Select a project-> NEW PROJECT` to create a new project to use our library.

Fill in the basic info and create the project.

![gt-create-app-1](images/gt-create-app-1.png)

## Enable YouTube DATA API service

Once the project created, the browser will redirect you to the project home page.

Click the `≡≡` symbol on the top left and select the `APIs & Services` tab.

You will see following info:

![gt-create-app-2](images/gt-create-app-2.png)

Click the `+ ENABLE APIS AND SERVICES` symbol, and input `YouTube DATA API` to search.

![gt-create-app-3](images/gt-create-app-3.png)

Chose the ``YouTube DATA API`` item.

![gt-create-app-4](images/gt-create-app-4.png)

Then click the `ENABLE` blue button. After a short period where the API is added to your project, the service will be activated.

## Create credentials

To use this API, you need credentials. Click `Create credentials` to get started.

![gt-create-app-5](images/gt-create-app-5.png)

You need to fill in some information to create credentials.

Just chose `YouTube DATA API v3`, `Other non-UI (e.g. cron job, daemon)` and `Public data`.

Then click the blue button `What credentials do I need?` to create.

![gt-create-app-6](images/gt-create-app-6.png)

You have now generated an api key.

Using this key, you can retrieve public YouTube data with our library

```python
from pyyoutube import Client

cli = Client(api_key="your api key")
```

Check out the [examples](https://github.com/sns-sdks/python-youtube/tree/master/examples) directory for some examples of using the library.

If you have an open source application using python-youtube, send me a link. I am very happy to add a link to it here.

If you want to get user data by OAuth. You need create the credential for ``OAuth client ID``.

You will find more information on OAth at the [Authorization](authorization.md) page.
