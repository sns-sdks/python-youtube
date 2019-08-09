import json


class BaseModel(object):
    """ Base model class  for instance use. """

    def __init__(self, **kwargs):
        self.param_defaults = {}

    def initial(self, kwargs):
        for (param, value) in self.param_defaults.items():
            setattr(self, param, kwargs.get(param, value))

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
            key_attr = getattr(self, key, None)
            # Notice:
            # Now have different handler to sub items
            if isinstance(key_attr, (list, tuple, set)):
                data[key] = list()
                for sub_obj in key_attr:
                    if getattr(sub_obj, 'as_dict', None):
                        data[key].append(sub_obj.as_dict())
                    else:
                        data[key].append(sub_obj)
            elif getattr(key_attr, 'as_dict', None):
                data[key] = key_attr.as_dict()
            elif key_attr is not None:
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


class ResourceId(BaseModel):
    """One ResourceId instance for playlistItem """

    def __init__(self, **kwargs):
        BaseModel.__init__(self, **kwargs)
        self.param_defaults = {
            'kind': None,
            'videoId': None
        }
        for (param, value) in self.param_defaults.items():
            setattr(self, param, kwargs.get(param, value))

    def __repr__(self):
        return "ResourceId(videoId={videoId},kind={title}".format(
            videoId=self.videoId, title=self.title
        )


class ChannelSnippet(BaseModel):
    """A class representing base info for channel snippet
    """

    def __init__(self, **kwargs):
        BaseModel.__init__(self, **kwargs)
        self.param_defaults = {
            'publishedAt': None,
            'title': None,
            'description': None,
            'defaultLanguage': None,
            'customUrl': None,
            'country': None,
            'thumbnails': None,
            'localized': None,
        }
        self.initial(kwargs)

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


class VideoSnippet(BaseModel):
    """A class representing base info for video snippet
    """

    def __init__(self, **kwargs):
        BaseModel.__init__(self, **kwargs)
        self.param_defaults = {
            'publishedAt': None,
            'title': None,
            'description': None,
            'defaultLanguage': None,
            'channelId': None,
            'channelTitle': None,
            'tags': None,
            'categoryId': None,
            'liveBroadcastContent': None,
            'defaultAudioLanguage': None,
            'thumbnails': None,
            'localized': None,
        }
        self.initial(kwargs)

    def __repr__(self):
        return "VideoSnippet(title={title}, description={description})".format(
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


class PlayListSnippet(BaseModel):
    def __init__(self, **kwargs):
        BaseModel.__init__(self, **kwargs)
        self.param_defaults = {
            'publishedAt': None,
            'title': None,
            'description': None,
            'channelId': None,
            'channelTitle': None,
            'thumbnails': None,
            'localized': None,
        }
        self.initial(kwargs)

    def __repr__(self):
        return "PlayListSnippet(title={title}, description={description})".format(
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


class PlaylistItemSnippet(BaseModel):
    """One PlaylistItemSnippet instance """

    def __init__(self, **kwargs):
        BaseModel.__init__(self, **kwargs)
        self.param_defaults = {
            "publishedAt": None,
            "channelId": None,
            "title": None,
            "description": None,
            "thumbnails": None,
            "channelTitle": None,
            "playlistId": None,
            "position": None,
            "resourceId": None
        }
        self.initial(kwargs)

    def __repr__(self):
        return "PlaylistItemSnippet(title={title},description={description})".format(
            title=self.title, description=self.description
        )

    @classmethod
    def new_from_json_dict(cls, data, **kwargs):
        thumbnails = data.get('thumbnails')
        if thumbnails:
            thumbnails = Thumbnails.new_from_json_dict(thumbnails)
        resource_id = data.get('resourceId')
        if resource_id:
            resource_id = ResourceId.new_from_json_dict(resource_id)
        return super(cls, cls).new_from_json_dict(
            data=data, thumbnails=thumbnails, resource_id=resource_id
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
            'hiddenSubscriberCount': None,
            'videoCount': None,
        }
        self.initial(kwargs)

    def __repr__(self):
        return "ChannelStatistics(subscriberCount={subscriberCount}, viewCount={viewCount})".format(
            subscriberCount=self.subscriberCount, viewCount=self.viewCount
        )


class VideoStatistics(BaseModel):
    """One VideoStatistics instance """

    def __init__(self, **kwargs):
        BaseModel.__init__(self, **kwargs)
        self.param_defaults = {
            'viewCount': None,
            'commentCount': None,
            'likeCount': None,
            'dislikeCount': None,
            'favoriteCount': None
        }
        self.initial(kwargs)

    def __repr__(self):
        return "VideoStatistics(viewCount={viewCount}, commentCount={commentCount})".format(
            viewCount=self.viewCount, commentCount=self.commentCount
        )


class RelatedPlaylists(BaseModel):
    """A class representing channel's related playlist info
    Some properties has been deprecated.
    Refer:
        https://developers.google.com/youtube/v3/docs/channels#contentDetails.relatedPlaylists
    """

    def __init__(self, **kwargs):
        BaseModel.__init__(self, **kwargs)
        self.param_defaults = {
            'favorites': None,
            'watchHistory': None,
            'watchLater': None,
            'uploads': None,
            'likes': None,
        }
        self.initial(kwargs)

    def __repr__(self):
        return "RelatedPlaylists(likes={likes}, uploads={uploads})".format(
            likes=self.likes, uploads=self.uploads
        )


class VideoRegionRestriction(BaseModel):
    def __init__(self, **kwargs):
        BaseModel.__init__(self, **kwargs)
        self.param_defaults = {
            'allowed': None,
            'blocked': None,
        }
        self.initial(kwargs)

    def __repr__(self):
        return "VideoRegionRestriction(allowed={allowed},blocked={blocked})".format(
            allowed=self.allowed, blocked=self.blocked
        )


class VideoContentRating(BaseModel):
    def __init__(self, **kwargs):
        BaseModel.__init__(self, **kwargs)
        self.param_defaults = {
            "acbRating": None,
            "agcomRating": None,
            "anatelRating": None,
            "bbfcRating": None,
            "bfvcRating": None,
            "bmukkRating": None,
            "catvRating": None,
            "catvfrRating": None,
            "cbfcRating": None,
            "cccRating": None,
            "cceRating": None,
            "chfilmRating": None,
            "chvrsRating": None,
            "cicfRating": None,
            "cnaRating": None,
            "cncRating": None,
            "csaRating": None,
            "cscfRating": None,
            "czfilmRating": None,
            "djctqRating": None,
            "djctqRatingReasons": None,
            "ecbmctRating": None,
            "eefilmRating": None,
            "egfilmRating": None,
            "eirinRating": None,
            "fcbmRating": None,
            "fcoRating": None,
            "fmocRating": None,
            "fpbRating": None,
            "fpbRatingReasons": None,
            "fskRating": None,
            "grfilmRating": None,
            "icaaRating": None,
            "ifcoRating": None,
            "ilfilmRating": None,
            "incaaRating": None,
            "kfcbRating": None,
            "kijkwijzerRating": None,
            "kmrbRating": None,
            "lsfRating": None,
            "mccaaRating": None,
            "mccypRating": None,
            "mcstRating": None,
            "mdaRating": None,
            "medietilsynetRating": None,
            "mekuRating": None,
            "mibacRating": None,
            "mocRating": None,
            "moctwRating": None,
            "mpaaRating": None,
            "mpaatRating": None,
            "mtrcbRating": None,
            "nbcRating": None,
            "nbcplRating": None,
            "nfrcRating": None,
            "nfvcbRating": None,
            "nkclvRating": None,
            "oflcRating": None,
            "pefilmRating": None,
            "rcnofRating": None,
            "resorteviolenciaRating": None,
            "rtcRating": None,
            "rteRating": None,
            "russiaRating": None,
            "skfilmRating": None,
            "smaisRating": None,
            "smsaRating": None,
            "tvpgRating": None,
            "ytRating": None

        }
        self.initial(kwargs)

    def __repr__(self):
        return "VideoContentRating(acbRating={acbRating})".format(
            acbRating=self.acbRating
        )


class ChannelContentDetails(BaseModel):
    """A class representing channel's content
    """

    def __init__(self, **kwargs):
        BaseModel.__init__(self, **kwargs)
        self.param_defaults = {
            'relatedPlaylists': None
        }
        self.initial(kwargs)

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


class VideoContentDetails(BaseModel):
    def __init__(self, **kwargs):
        BaseModel.__init__(self, **kwargs)
        self.param_defaults = {
            'duration': None,
            'dimension': None,
            'caption': None,
            'licensedContent': None,
            'projection': None,
            'hasCustomThumbnail': None,
            'regionRestriction': None,
            'contentRating': None,
        }
        self.initial(kwargs)

    @classmethod
    def new_from_json_dict(cls, data, **kwargs):
        region_restriction = data.get('regionRestriction')
        if region_restriction:
            region_restriction = VideoRegionRestriction.new_from_json_dict(region_restriction)
        content_rating = data.get('contentRating')
        if content_rating:
            content_rating = VideoContentRating.new_from_json_dict(content_rating)
        return super(cls, cls).new_from_json_dict(
            data=data,
            region_restriction=region_restriction, content_rating=content_rating
        )


class PlayListContentDetails(BaseModel):
    """A class representing playlist's content
    """

    def __init__(self, **kwargs):
        BaseModel.__init__(self, **kwargs)
        self.param_defaults = {
            'itemCount': None
        }
        self.initial(kwargs)

    def __repr__(self):
        return "PlayListContentDetails(itemCount={itemCount})".format(
            itemCount=self.itemCount
        )


class PlaylistItemContentDetails(BaseModel):
    """One PlaylistItemContentDetails instance """

    def __init__(self, **kwargs):
        BaseModel.__init__(self, **kwargs)
        self.param_defaults = {
            'videoId': None,
            'videoPublishedAt': None
        }
        self.initial(kwargs)

    def __repr__(self):
        return "PlaylistItemContentDetails(videoId={videoId},videoPublishedAt={videoPublishedAt)".format(
            videoId=self.videoId, videoPublishedAt=self.videoPublishedAt
        )


class Topic(BaseModel):
    """A class representing Topic info"""

    def __init__(self, **kwargs):
        BaseModel.__init__(self, **kwargs)
        self.param_defaults = {
            'id': None,
            'description': None  # convert id to topic desc
        }
        self.initial(kwargs)

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
        self.initial(kwargs)

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
        self.param_defaults = {
            'privacyStatus': None,
            'isLinked': None,
            'longUploadsStatus': None,
        }
        self.initial(kwargs)

    def __repr__(self):
        return "ChannelStatus(privacyStatus={privacyStatus})".format(privacyStatus=self.privacyStatus)


class VideoStatus(BaseModel):
    def __init__(self, **kwargs):
        BaseModel.__init__(self, **kwargs)
        self.param_defaults = {
            'privacyStatus': None,
            'uploadStatus': None,
            'failureReason': None,
            'rejectionReason': None,
            'publishAt': None,
            'license': None,
            'embeddable': None,
        }
        self.initial(kwargs)

    def __repr__(self):
        return "VideoStatus(privacyStatus={privacyStatus}, publishAt={publishAt})".format(
            privacyStatus=self.privacyStatus, publishAt=self.publishAt
        )


class PlayListStatus(BaseModel):
    def __init__(self, **kwargs):
        BaseModel.__init__(self, **kwargs)
        self.param_defaults = {
            'privacyStatus': None
        }
        self.initial(kwargs)

    def __repr__(self):
        return "PlayListStatus(privacyStatus={privacyStatus})".format(
            privacyStatus=self.privacyStatus
        )


class PlaylistItemStatus(BaseModel):
    def __init__(self, **kwargs):
        BaseModel.__init__(self, **kwargs)
        self.param_defaults = {
            'privacyStatus': None
        }
        self.initial(kwargs)

    def __repr__(self):
        return "PlaylistItemStatus(privacyStatus={privacyStatus})".format(
            privacyStatus=self.privacyStatus
        )


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
        self.initial(kwargs)


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
        self.initial(kwargs)

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
        self.initial(kwargs)

    def __repr__(self):
        return "Channel(id={c_id},kind={kind})".format(c_id=self.id, kind=self.kind)

    @classmethod
    def new_from_json_dict(cls, data, **kwargs):
        json_data = data.copy()
        if 'snippet' in json_data:
            json_data['snippet'] = ChannelSnippet.new_from_json_dict(data['snippet'])
        if 'contentDetails' in json_data:
            json_data['contentDetails'] = ChannelContentDetails.new_from_json_dict(data['contentDetails'])
        if 'statistics' in json_data:
            json_data['statistics'] = ChannelStatistics.new_from_json_dict(data['statistics'])
        if 'status' in json_data:
            json_data['status'] = ChannelStatus.new_from_json_dict(data['status'])

        if kwargs:
            for key, val in kwargs.items():
                json_data[key] = val
        c = cls(**json_data)
        c._json = data
        return c


class Video(BaseModel):
    """ One video info instance """

    def __init__(self, **kwargs):
        BaseModel.__init__(self, **kwargs)
        self.param_defaults = {
            'kind': None,
            'etag': None,
            'id': None,
            'snippet': None,
            'contentDetails': None,
            'statistics': None,
            'status': None,
        }
        self.initial(kwargs)

    def __repr__(self):
        return "Video(id={v_id},kind={kind})".format(v_id=self.id, kind=self.kind)

    @classmethod
    def new_from_json_dict(cls, data, **kwargs):
        json_data = data.copy()
        if 'snippet' in json_data:
            json_data['snippet'] = VideoSnippet.new_from_json_dict(data['snippet'])
        if 'contentDetails' in json_data:
            json_data['contentDetails'] = VideoContentDetails.new_from_json_dict(data['contentDetails'])
        if 'statistics' in json_data:
            json_data['statistics'] = VideoStatistics.new_from_json_dict(data['statistics'])
        if 'status' in json_data:
            json_data['status'] = VideoStatus.new_from_json_dict(data['status'])

        if kwargs:
            for key, val in kwargs.items():
                json_data[key] = val
        c = cls(**json_data)
        c._json = data
        return c


class PlayList(BaseModel):
    """ One playlist info instance. """

    def __init__(self, **kwargs):
        BaseModel.__init__(self, **kwargs)
        self.param_defaults = {
            'kind': None,
            'etag': None,
            'id': None,
            'snippet': None,
            'contentDetails': None,
            'status': None,
        }
        self.initial(kwargs)

    def __repr__(self):
        return "Playlist(id={p_id},kind={kind})".format(
            p_id=self.id, kind=self.kind
        )

    @classmethod
    def new_from_json_dict(cls, data, **kwargs):
        json_data = data.copy()
        if 'snippet' in json_data:
            json_data['snippet'] = PlayListSnippet.new_from_json_dict(data['snippet'])
        if 'contentDetails' in json_data:
            json_data['contentDetails'] = PlayListContentDetails.new_from_json_dict(data['contentDetails'])
        if 'status' in json_data:
            json_data['status'] = PlayListStatus.new_from_json_dict(data['status'])

        if kwargs:
            for key, val in kwargs.items():
                json_data[key] = val
        c = cls(**json_data)
        c._json = data
        return c


class PlaylistItem(BaseModel):
    """One PlaylistItem instance"""

    def __init__(self, **kwargs):
        BaseModel.__init__(self, **kwargs)
        self.param_defaults = {
            'kind': None,
            'etag': None,
            'id': None,
            'snippet': None,
            'contentDetails': None,
            'status': None,
        }
        self.initial(kwargs)

    def __repr__(self):
        return "PlaylistItem(id={p_id},kind={kind})".format(
            p_id=self.id, kind=self.kind
        )

    @classmethod
    def new_from_json_dict(cls, data, **kwargs):
        json_data = data.copy()
        if 'snippet' in json_data:
            json_data['snippet'] = PlaylistItemSnippet.new_from_json_dict(data['snippet'])
        if 'contentDetails' in json_data:
            json_data['contentDetails'] = PlaylistItemContentDetails.new_from_json_dict(data['contentDetails'])
        if 'status' in json_data:
            json_data['status'] = PlaylistItemStatus.new_from_json_dict(data['status'])

        if kwargs:
            for key, val in kwargs.items():
                json_data[key] = val
        c = cls(**json_data)
        c._json = data
        return c
