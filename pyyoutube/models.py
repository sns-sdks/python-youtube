import json


class BaseModel(object):
    """ Base model class  for instance use. """

    def __init__(self, **kwargs):
        self.param_defaults = {}

    @classmethod
    def new_from_json_dict(cls, data, **kwargs):
        """ convert the data from api to model's properties. """
        json_data = data.copy()
        if kwargs:
            for key, val in kwargs.items():
                json_data[key] = val
        c = cls(**json_data)
        c.__json = data
        return c

    def as_dict(self):
        """ Create a dictionary representation of the object. To convert all model properties. """
        data = {}
        for (key, value) in self.param_defaults.items():
            data[key] = getattr(self, key, None)
        return data

    def as_json_string(self):
        """ Create a json string representation of the object. To convert all model properties. """
        return json.dumps(self.as_dict(), sort_keys=True)


class AccessToken(BaseModel):
    def __init__(self, **kwargs):
        BaseModel.__init__(self, **kwargs)
        self.param_defaults = {
            'access_token': None,
            'expires_in': None,
            'refresh_token': None,
            'scope': None,
            'token_type': None,
            'id_token': None
        }

        for (param, value) in self.param_defaults.items():
            setattr(self, param, kwargs.get(param, value))
            if param == 'scope':
                self.scope = self.scope.split(' ')

    def __repr__(self):
        return "AccessToken(access_token={token}, expires_in={ex})".format(
            token=self.access_token,
            ex=self.expires_in
        )


class UserProfile(BaseModel):
    def __init__(self, **kwargs):
        BaseModel.__init__(self, **kwargs)
        self.param_defaults = {
            'id': None,
            'name': None,
            'given_name': None,
            'family_name': None,
            'picture': None,
            'locale': None
        }

        for (param, value) in self.param_defaults.items():
            setattr(self, param, kwargs.get(param, value))

    def __repr__(self):
        return "User(ID={u_id}, name={name})".format(
            u_id=self.id,
            name=self.name
        )


class Thumbnail(BaseModel):
    """a class for the image resource.
    """

    def __init__(self, **kwargs):
        BaseModel.__init__(self, **kwargs)
        self.param_defaults = {
            'url': None,
            'width': None,
            'height': None
        }

        for (param, value) in self.param_defaults.items():
            setattr(self, param, kwargs.get(param, value))

    def __repr__(self):
        return "Thumbnail(url={url}".format(url=self.url)


class Thumbnails(BaseModel):
    """a class for the multi image resource.
    """

    def __init__(self, **kwargs):
        BaseModel.__init__(self, **kwargs)
        self.param_defaults = {
            'default': None,
            'medium': None,
            'high': None,
            'standard': None,
            'maxres': None,
        }

        for (param, value) in self.param_defaults.items():
            setattr(self, param, kwargs.get(param, value))

    @classmethod
    def new_from_json_dict(cls, data, **kwargs):
        from pyyoutube import Thumbnail
        params = {}
        for (key, value) in data.items():
            thumbnail = Thumbnail.new_from_json_dict(value)
            params[key] = thumbnail
        c = cls(**params)
        c.__json = data
        return c


class Localized(BaseModel):
    """A class for point or given language to retrieve the resource info.
    """

    def __init__(self, **kwargs):
        BaseModel.__init__(self, **kwargs)
        self.param_defaults = {
            'title': None,
            'description': None
        }
        for (param, value) in self.param_defaults.items():
            setattr(self, param, kwargs.get(param, value))

    def __repr__(self):
        return "Localized(title={title}".format(title=self.title)


class ChannelSnippet(BaseModel):
    """A class representing base info for channel
    """

    def __init__(self, **kwargs):
        BaseModel.__init__(self, **kwargs)
        self.param_defaults = {
            'title': None,
            'description': None,
            'customUrl': None,
            'publishedAt': None,
            'defaultLanguage': None,  # language for title and description.
            'country': None,
            'thumbnails': None,
            'localized': None,
        }
        for (param, value) in self.param_defaults.items():
            setattr(self, param, kwargs.get(param, value))

    def __repr__(self):
        return "ChannelSnippet(title={title}, description={description})".format(
            title=self.title, description=self.description
        )

    @classmethod
    def new_from_json_dict(cls, data, **kwargs):
        thumbnails = data.get('thumbnails')
        if thumbnails:
            thumbnails = Thumbnails.new_from_json_dict(thumbnails)
        localized = data.get('localized')
        if localized:
            localized = Localized.new_from_json_dict(localized)
        return super(cls, cls).new_from_json_dict(
            data=data, thumbnails=thumbnails, localized=localized
        )


class ChannelStatistics(BaseModel):
    """A class representing Channel's statistics data.
    """

    def __init__(self, **kwargs):
        BaseModel.__init__(self, **kwargs)
        self.param_defaults = {
            'viewCount': None,
            'commentCount': None,
            'subscriberCount': None,
            'hiddenSubscriberCount': False,
            'videoCount': None
        }
        for (param, value) in self.param_defaults.items():
            setattr(self, param, kwargs.get(param, value))

    def __repr__(self):
        return "ChannelStatistics(subscriberCount={subscriberCount}, viewCount={viewCount})".format(
            subscriberCount=self.subscriberCount, viewCount=self.viewCount
        )


class RelatedPlaylists(BaseModel):
    """A class representing channel's related playlist info
    """

    def __init__(self, **kwargs):
        BaseModel.__init__(self, **kwargs)
        self.param_defaults = {
            'uploads': None,
            'likes': None,
        }
        for (param, value) in self.param_defaults.items():
            setattr(self, param, kwargs.get(param, value))

    def __repr__(self):
        return "RelatedPlaylists(likes={likes}, uploads={uploads})".format(
            likes=self.likes, uploads=self.uploads
        )


class ChannelContentDetails(BaseModel):
    """A class representing channel's content
    """

    def __init__(self, **kwargs):
        BaseModel.__init__(self, **kwargs)
        self.param_defaults = {
            'relatedPlaylists': None,
        }
        for (param, value) in self.param_defaults.items():
            setattr(self, param, kwargs.get(param, value))

    def __repr__(self):
        return "ChannelContentDetails(relatedPlaylists={relatedPlaylists})".format(
            relatedPlaylists=self.relatedPlaylists
        )

    @classmethod
    def new_from_json_dict(cls, data, **kwargs):
        related_playlists = data.get('relatedPlaylists')
        if related_playlists:
            related_playlists = RelatedPlaylists.new_from_json_dict(related_playlists)
        return super(cls, cls).new_from_json_dict(data=data, relatedPlaylists=related_playlists)


class Topic(BaseModel):
    """A class representing Topic info"""

    def __init__(self, **kwargs):
        BaseModel.__init__(self, **kwargs)
        self.param_defaults = {
            'id': None,
            'description': None  # convert id to topic desc
        }
        for (param, value) in self.param_defaults.items():
            setattr(self, param, kwargs.get(param, value))

    def __repr__(self):
        return "Topic(id={t_id},description={desc})".format(t_id=self.id, desc=self.description)

    @classmethod
    def new_from_json_dict(cls, data, **kwargs):
        from pyyoutube import CHANNEL_TOPICS
        desc = CHANNEL_TOPICS.get(data)
        json_data = {
            'id': data,
            'description': desc,
        }
        if kwargs:
            for key, val in kwargs.items():
                json_data[key] = val

        c = cls(**json_data)
        c.__json = data
        return c


class ChannelTopicDetails(BaseModel):
    """A class representing channel's topic detail info
    """

    def __init__(self, **kwargs):
        BaseModel.__init__(self, **kwargs)
        self.topicIds = None
        self.param_defaults = {
            'topicIds': None,
            'topicCategories': None
        }
        for (param, value) in self.param_defaults.items():
            setattr(self, param, kwargs.get(param, value))

    def __repr__(self):
        if self.topicIds is not None:
            display = self.topicIds[0]
        else:
            display = None
        return "ChannelTopicDetails(topicIds={display})".format(display=display)

    @classmethod
    def new_from_json_dict(cls, data, **kwargs):
        json_data = data.copy()
        for key, value in data.items():
            if key == 'topicIds':
                json_data[key] = [Topic.new_from_json_dict(item) for item in value]
            else:
                json_data[key] = value
        if kwargs:
            for key, val in kwargs.items():
                json_data[key] = val

        c = cls(**json_data)
        c.__json = data
        return c


class ChannelStatus(BaseModel):
    """A class representing channel's status
    """

    def __init__(self, **kwargs):
        BaseModel.__init__(self, **kwargs)
        self.privacyStatus = None
        self.param_defaults = {
            'privacyStatus': None,
            'isLinked': None,
            'longUploadsStatus': None
        }
        for (param, value) in self.param_defaults.items():
            setattr(self, param, kwargs.get(param, value))

    def __repr__(self):
        return "ChannelStatus(privacyStatus={privacyStatus})".format(privacyStatus=self.privacyStatus)


class ChannelBrandingChannel(BaseModel):
    """A class representing branding setting's channel info
    """

    def __init__(self, **kwargs):
        BaseModel.__init__(self, **kwargs)
        self.title = None
        self.description = None
        self.param_defaults = {
            'title': None,
            'description': None,
            'keywords': None,
            'defaultTab': None,
            'trackingAnalyticsAccountId': None,
            'moderateComments': None,
            'showRelatedChannels': None,
            'showBrowseView': None,
            'featuredChannelsTitle': None,
            'featuredChannelsUrls': None,
            'unsubscribedTrailer': None,
            'profileColor': None,
            'defaultLanguage': None,
            'country': None,
        }
        for (param, value) in self.param_defaults.items():
            setattr(self, param, kwargs.get(param, value))

    def __repr__(self):
        return "ChannelBrandingChannel(title={title},description={desc})".format(
            title=self.title, desc=self.description
        )


class ChannelBrandingImage(BaseModel):
    def __init__(self, **kwargs):
        BaseModel.__init__(self, **kwargs)
        self.param_defaults = {
            'bannerImageUrl': None,
            'bannerMobileImageUrl': None,
            'watchIconImageUrl': None,
            'trackingImageUrl': None,
            'bannerTabletLowImageUrl': None,
            'bannerTabletImageUrl': None,
            'bannerTabletHdImageUrl': None,
            'bannerTabletExtraHdImageUrl': None,
            'bannerMobileLowImageUrl': None,
            'bannerMobileMediumHdImageUrl': None,
            'bannerMobileHdImageUrl': None,
            'bannerMobileExtraHdImageUrl': None,
            'bannerTvImageUrl': None,
            'bannerTvLowImageUrl': None,
            'bannerTvMediumImageUrl': None,
            'bannerTvHighImageUrl': None,
            'bannerExternalUrl': None,
        }
        for (param, value) in self.param_defaults.items():
            setattr(self, param, kwargs.get(param, value))


class ChannelBrandingHint(BaseModel):
    def __init__(self, **kwargs):
        BaseModel.__init__(self, **kwargs)
        self.param_defaults = {
            'property': None,
            'value': None
        }
        for (param, value) in self.param_defaults.items():
            setattr(self, param, kwargs.get(param, value))


class ChannelBrandingSetting(BaseModel):
    def __init__(self, **kwargs):
        BaseModel.__init__(self, **kwargs)
        self.param_defaults = {
            'channel': None,
            'image': None,
            'hints': None,
        }
        for (param, value) in self.param_defaults.items():
            setattr(self, param, kwargs.get(param, value))

    @classmethod
    def new_from_json_dict(cls, data, **kwargs):
        channel = data.get('channel')
        if channel is not None:
            channel = ChannelBrandingChannel.new_from_json_dict(channel)
        image = data.get('image')
        if image is not None:
            image = ChannelBrandingImage.new_from_json_dict(image)
        hints = data.get('hints')
        if hints is not None:
            hints = [ChannelBrandingHint.new_from_json_dict(item) for item in hints]

        json_data = {
            'channel': channel,
            'image': image,
            'hints': hints
        }
        c = cls(**json_data)
        c.__json = data
        return c


class Channel(BaseModel):
    def __init__(self, **kwargs):
        BaseModel.__init__(self, **kwargs)
        self.id = None
        self.kind = None
        self.param_defaults = {
            'kind': None,
            'etag': None,
            'id': None,
            'snippet': None,
            'contentDetails': None,
            'statistics': None,
            'topicDetails': None,
            'status': None,
            'brandingSettings': None
        }
        for (param, value) in self.param_defaults.items():
            setattr(self, param, kwargs.get(param, value))

    def __repr__(self):
        return "Channel(id={id},kind={kind})".format(id=self.id, kind=self.kind)

    @classmethod
    def new_from_json_dict(cls, data, **kwargs):
        json_data = data.copy()
        if 'snippet' in json_data:
            json_data['snippet'] = ChannelSnippet.new_from_json_dict(data['snippet'])
        if 'contentDetails' in json_data:
            json_data['contentDetails'] = ChannelContentDetails.new_from_json_dict(data['contentDetails'])
        if 'statistics' in json_data:
            json_data['statistics'] = ChannelStatistics.new_from_json_dict(data['statistics'])
        if 'topicDetails' in json_data:
            json_data['topicDetails'] = ChannelTopicDetails.new_from_json_dict(data['topicDetails'])
        if 'status' in json_data:
            json_data['status'] = ChannelStatus.new_from_json_dict(data['status'])
        if 'brandingSettings' in json_data:
            json_data['brandingSettings'] = ChannelBrandingSetting.new_from_json_dict(data['brandingSettings'])

        if kwargs:
            for key, val in kwargs.items():
                json_data[key] = val
        c = cls(**json_data)
        c._json = data
        return c
