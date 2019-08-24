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
    """
    A class representing access toke for api.
    Refer: https://developers.google.com/youtube/v3/guides/auth/installed-apps
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
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
            # Refer https://developers.google.com/identity/protocols/googlescopes
            if param == 'scope':
                self.scope = self.scope.split(' ')

    def __repr__(self):
        return f"AccessToken(access_token={self.access_token}, expires_in={self.expires_in})"


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
    """
    A class representing the thumbnail resource info.
    Refer: https://developers.google.com/youtube/v3/docs/channels#snippet.thumbnails.(key).url
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.param_defaults = {
            'url': None,
            'width': None,
            'height': None
        }
        self.initial(kwargs)

    def __repr__(self):
        return f"Thumbnail(url={self.url}"


class Thumbnails(BaseModel):
    """
    A class representing the multi thumbnail resource info.
    Refer: https://developers.google.com/youtube/v3/docs/channels#snippet.thumbnails
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.param_defaults = {
            'default': None,
            'medium': None,
            'high': None,
            'standard': None,
            'maxres': None,
        }
        self.initial(kwargs)

    @classmethod
    def new_from_json_dict(cls, data, **kwargs):
        new_data = {}
        for (key, value) in data.items():
            thumbnail = Thumbnail.new_from_json_dict(value)
            new_data[key] = thumbnail
        return super().new_from_json_dict(new_data)


class ChannelBrandingChannel(BaseModel):
    """
    A class representing channel branding setting's channel info.
    Refer: https://developers.google.com/youtube/v3/docs/channels#brandingSettings.channel
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
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
        self.initial(kwargs)

    def __repr__(self):
        return f"ChannelBrandingChannel(title={self.title},description={self.description})"


class ChannelBrandingHint(BaseModel):
    """
    A class representing channel branding setting's hint info.
    Refer: https://developers.google.com/youtube/v3/docs/channels#brandingSettings.hints
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.param_defaults = {
            'property': None,
            'value': None,
        }
        self.initial(kwargs)

    def __repr__(self):
        return f"ChannelBrandingHint(property={self.property})"


class ChannelBrandingImage(BaseModel):
    """
       A class representing channel branding setting's image info.
       Refer: https://developers.google.com/youtube/v3/docs/channels#brandingSettings.image
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
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

    def __repr__(self):
        return f"ChannelBrandingImage(bannerImageUrl={self.bannerImageUrl})"


class ChannelBrandingSetting(BaseModel):
    """
    A class representing the channel branding settings info.
    Refer: https://developers.google.com/youtube/v3/docs/channels#brandingSettings
    """

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
        return super().new_from_json_dict(
            data=data, channel=channel, image=image,
            hints=hints
        )


class ChannelContentDetails(BaseModel):
    """
    A class representing channel's content info.
    Refer: https://developers.google.com/youtube/v3/docs/channels#contentDetails
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.param_defaults = {
            'relatedPlaylists': None
        }
        self.initial(kwargs)

    def __repr__(self):
        return f"ChannelContentDetails(relatedPlaylists={self.relatedPlaylists})"

    @classmethod
    def new_from_json_dict(cls, data, **kwargs):
        related_playlists = data.get('relatedPlaylists')
        if related_playlists:
            related_playlists = RelatedPlaylists.new_from_json_dict(related_playlists)
        return super().new_from_json_dict(
            data=data, relatedPlaylists=related_playlists
        )


class Topic(BaseModel):
    """
    A class representing Topic info.
    Refer: https://developers.google.com/youtube/v3/docs/channels#topicDetails.topicIds[]
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.param_defaults = {
            'id': None,
            'description': None  # convert id to topic desc
        }
        self.initial(kwargs)

    def __repr__(self):
        return f"Topic(id={self.id},description={self.description})"

    @classmethod
    def new_from_json_dict(cls, data, **kwargs):
        # custom to build topic info
        from pyyoutube import CHANNEL_TOPICS
        desc = CHANNEL_TOPICS.get(data)
        return super().new_from_json_dict(data={}, id=data, description=desc)


class ChannelTopicDetails(BaseModel):
    """
    A class representing channel's topic detail info.
    Refer: https://developers.google.com/youtube/v3/docs/channels#topicDetails
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
        return f"ChannelTopicDetails(topicIds={self.topicIds})"

    @classmethod
    def new_from_json_dict(cls, data, **kwargs):
        topic_ids = data.get('topicIds')
        if topic_ids is not None:
            topic_ids = [Topic.new_from_json_dict(item) for item in topic_ids]
        return super().new_from_json_dict(data=data, topicIds=topic_ids)


class Localized(BaseModel):
    """
    A class representing the channel snippet localized info.
    Refer: https://developers.google.com/youtube/v3/docs/channels#snippet.localized
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.param_defaults = {
            'title': None,
            'description': None
        }
        self.initial(kwargs)

    def __repr__(self):
        return f"Localized(title={self.title}"


class ChannelSnippet(BaseModel):
    """
    A class representing base info for channel snippet info.
    Refer: https://developers.google.com/youtube/v3/docs/channels#snippet
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
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
        return f"ChannelSnippet(title={self.title}, description={self.description})"

    @classmethod
    def new_from_json_dict(cls, data, **kwargs):
        thumbnails = data.get('thumbnails')
        if thumbnails:
            thumbnails = Thumbnails.new_from_json_dict(thumbnails)
        localized = data.get('localized')
        if localized:
            localized = Localized.new_from_json_dict(localized)
        return super().new_from_json_dict(
            data=data, thumbnails=thumbnails, localized=localized
        )


class ChannelStatistics(BaseModel):
    """
    A class representing Channel's statistics info.
    Refer: https://developers.google.com/youtube/v3/docs/channels#statistics
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.param_defaults = {
            'viewCount': None,
            'commentCount': None,
            'subscriberCount': None,
            'hiddenSubscriberCount': None,
            'videoCount': None,
        }
        self.initial(kwargs)

    def __repr__(self):
        return f"ChannelStatistics(subscriberCount={self.subscriberCount}, viewCount={self.viewCount})"


class ChannelStatus(BaseModel):
    """
    A class representing channel's status info.
    Refer: https://developers.google.com/youtube/v3/docs/channels#status
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.param_defaults = {
            'privacyStatus': None,
            'isLinked': None,
            'longUploadsStatus': None,
        }
        self.initial(kwargs)

    def __repr__(self):
        return f"ChannelStatus(privacyStatus={self.privacyStatus})"


class Channel(BaseModel):
    """
    A class representing channel's info.
    Refer: https://developers.google.com/youtube/v3/docs/channels
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
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
        return f"Channel(id={self.id},kind={self.kind})"

    @classmethod
    def new_from_json_dict(cls, data, **kwargs):
        snippet = data.get('snippet')
        if snippet is not None:
            snippet = ChannelSnippet.new_from_json_dict(snippet)
        content_details = data.get('contentDetails')
        if content_details is not None:
            content_details = ChannelContentDetails.new_from_json_dict(content_details)
        statistics = data.get('statistics')
        if statistics is not None:
            statistics = ChannelStatistics.new_from_json_dict(statistics)
        status = data.get('status')
        if status is not None:
            status = ChannelStatus.new_from_json_dict(status)
        return super().new_from_json_dict(
            data=data, snippet=snippet,
            contentDetails=content_details, statistics=statistics,
            status=status
        )


class VideoContentDetails(BaseModel):
    """
    A class representing the video content details info.
    Refer: https://developers.google.com/youtube/v3/docs/videos#contentDetails
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.param_defaults = {
            'duration': None,
            'dimension': None,
            'definition': None,
            'caption': None,
            'licensedContent': None,
            'projection': None,
        }
        self.initial(kwargs)

    def __repr__(self):
        return f"VideoContentDetails(dimension={self.dimension},duration={self.duration})"


class VideoTopicDetails(BaseModel):
    """
    A class representing video's topic detail info.
    Refer: https://developers.google.com/youtube/v3/docs/videos#topicDetails
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.topicIds = None
        self.param_defaults = {
            'topicIds': None,
            'relevantTopicIds': None,
            'topicCategories': None
        }
        self.initial(kwargs)

    def __repr__(self):
        return f"VideoTopicDetails(topicIds={self.topicIds})"

    @classmethod
    def new_from_json_dict(cls, data, **kwargs):
        topic_ids = data.get('topicIds')
        if topic_ids is not None:
            topic_ids = [Topic.new_from_json_dict(item) for item in topic_ids]
        relevant_topic_ids = data.get('relevantTopicIds')
        if relevant_topic_ids is not None:
            relevant_topic_ids = [Topic.new_from_json_dict(item) for item in relevant_topic_ids]

        return super().new_from_json_dict(
            data=data, topicIds=topic_ids,
            relevantTopicIds=relevant_topic_ids
        )


class VideoSnippet(BaseModel):
    """
    A class representing the video snippet info.
    Refer: https://developers.google.com/youtube/v3/docs/videos#snippet
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.param_defaults = {
            'publishedAt': None,
            'channelId': None,
            'title': None,
            'description': None,
            'thumbnails': None,
            'channelTitle': None,
            'tags': None,
            'categoryId': None,
            'liveBroadcastContent': None,
            'defaultLanguage': None,
            'localized': None,
            'defaultAudioLanguage': None,
        }
        self.initial(kwargs)

    def __repr__(self):
        return f"VideoSnippet(title={self.title}, description={self.description})"

    @classmethod
    def new_from_json_dict(cls, data, **kwargs):
        thumbnails = data.get('thumbnails')
        if thumbnails:
            thumbnails = Thumbnails.new_from_json_dict(thumbnails)
        localized = data.get('localized')
        if localized:
            localized = Localized.new_from_json_dict(localized)
        return super().new_from_json_dict(
            data=data, thumbnails=thumbnails, localized=localized
        )


class VideoStatistics(BaseModel):
    """
    A class representing the video statistics info.
    Refer: https://developers.google.com/youtube/v3/docs/videos#statistics
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.param_defaults = {
            'viewCount': None,
            'likeCount': None,
            'dislikeCount': None,
            'favoriteCount': None,  # This property has been deprecated.
            'commentCount': None,
        }
        self.initial(kwargs)

    def __repr__(self):
        return f"VideoStatistics(viewCount={self.viewCount}, commentCount={self.commentCount})"


class VideoStatus(BaseModel):
    """
    A class representing the video status info.
    Refer: https://developers.google.com/youtube/v3/docs/videos#status
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.param_defaults = {
            'uploadStatus': None,
            'failureReason': None,
            'rejectionReason': None,
            'privacyStatus': None,
            'publishAt': None,
            'license': None,
            'embeddable': None,
            'publicStatsViewable': None
        }
        self.initial(kwargs)

    def __repr__(self):
        return f"VideoStatus(privacyStatus={self.privacyStatus}, publishAt={self.publishAt})"


class Video(BaseModel):
    """
    A class representing the video info.
    # TODO now only handle the public info.
    Refer: https://developers.google.com/youtube/v3/docs/videos
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.param_defaults = {
            'kind': None,
            'etag': None,
            'id': None,
            'snippet': None,
            'contentDetails': None,
            'status': None,
            'statistics': None,
            'topicDetails': None,
        }
        self.initial(kwargs)

    def __repr__(self):
        return f"Video(id={self.id},kind={self.kind})"

    @classmethod
    def new_from_json_dict(cls, data, **kwargs):
        snippet = data.get('snippet')
        if snippet is not None:
            snippet = VideoSnippet.new_from_json_dict(snippet)
        content_details = data.get('contentDetails')
        if content_details is not None:
            content_details = VideoContentDetails.new_from_json_dict(content_details)
        topic_details = data.get('topicDetails')
        if topic_details is not None:
            topic_details = VideoTopicDetails.new_from_json_dict(topic_details)
        statistics = data.get('statistics')
        if statistics is not None:
            statistics = VideoStatistics.new_from_json_dict(statistics)
        status = data.get('status')
        if status is not None:
            status = VideoStatus.new_from_json_dict(status)
        return super().new_from_json_dict(
            data=data, snippet=snippet,
            contentDetails=content_details, topicDetails=topic_details,
            statistics=statistics, status=status
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
        snippet = data.get('snippet')
        if snippet is not None:
            snippet = PlayListSnippet.new_from_json_dict(snippet)
        content_details = data.get('contentDetails')
        if content_details is not None:
            content_details = PlayListContentDetails.new_from_json_dict(content_details)
        status = data.get('status')
        if status is not None:
            status = PlayListStatus.new_from_json_dict(status)
        return super().new_from_json_dict(
            data=data, snippet=snippet,
            contentDetails=content_details, status=status
        )


class ResourceId(BaseModel):
    """
    A class representing
    """

    def __init__(self, **kwargs):
        BaseModel.__init__(self, **kwargs)
        self.param_defaults = {
            'kind': None,
            'videoId': None
        }
        for (param, value) in self.param_defaults.items():
            setattr(self, param, kwargs.get(param, value))

    def __repr__(self):
        return f"ResourceId(videoId={self.videoId},kind={self.kind}"


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
        return f"PlaylistItemContentDetails(videoId={self.videoId},videoPublishedAt={self.videoPublishedAt}"


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

        snippet = data.get('snippet')
        if snippet is not None:
            snippet = PlaylistItemSnippet.new_from_json_dict(snippet)
        content_details = data.get('contentDetails')
        if content_details is not None:
            content_details = PlaylistItemContentDetails.new_from_json_dict(content_details)
        status = data.get('status')
        if status is not None:
            status = PlaylistItemStatus.new_from_json_dict(status)
        return super().new_from_json_dict(
            data=data, snippet=snippet,
            contentDetails=content_details, status=status
        )


class CommentSnippet(BaseModel):
    """
    A class representing comment's snippet info.
    Refer: https://developers.google.com/youtube/v3/docs/comments#snippet
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.param_defaults = {
            'authorDisplayName': None,
            'authorProfileImageUrl': None,
            'authorChannelUrl': None,
            'authorChannelId': None,
            'channelId': None,
            'videoId': None,
            'textDisplay': None,
            'textOriginal': None,
            'parentId': None,
            'canRate': None,
            'viewerRating': None,
            'likeCount': None,
            'moderationStatus': None,
            'publishedAt': None,
            'updatedAt': None,
        }
        self.initial(kwargs)

    def __repr__(self):
        return f"CommentSnippet(author=f{self.authorDisplayName},likeCount={self.likeCount})"


class Comment(BaseModel):
    """
    A class representing comment info.
    Refer: https://developers.google.com/youtube/v3/docs/comments
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.param_defaults = {
            'kind': None,
            'etag': None,
            'id': None,
            'snippet': None
        }
        self.initial(kwargs)

    def __repr__(self):
        return f"Comment(id={self.id},kind={self.kind})"

    @classmethod
    def new_from_json_dict(cls, data, **kwargs):
        snippet = data.get('snippet')
        if snippet is not None:
            snippet = CommentSnippet.new_from_json_dict(snippet)
        return super().new_from_json_dict(
            data=data, snippet=snippet
        )


class CommentTreadSnippet(BaseModel):
    """
    A class representing comment tread snippet info.
    Refer: https://developers.google.com/youtube/v3/docs/commentThreads#snippet
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.param_defaults = {
            'channelId': None,
            'videoId': None,
            'topLevelComment': None,
            'canReply': None,
            'totalReplyCount': None,
            'isPublic': None
        }
        self.initial(kwargs)

    def __repr__(self):
        return f'CommentTreadSnippet(channelId={self.channelId},videoId={self.videoId})'

    @classmethod
    def new_from_json_dict(cls, data, **kwargs):
        top_level_comment = data.get('topLevelComment')
        if top_level_comment is not None:
            top_level_comment = Comment.new_from_json_dict(top_level_comment)

        return super().new_from_json_dict(
            data=data, topLevelComment=top_level_comment
        )


class CommentTreadReplies(BaseModel):
    """
    A class representing comment tread replies info.
    Refer: https://developers.google.com/youtube/v3/docs/commentThreads#replies
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.param_defaults = {
            'comments': [],
        }
        self.initial(kwargs)

    def __repr__(self):
        return f'Replies(count={len(self.comments)})'

    @classmethod
    def new_from_json_dict(cls, data, **kwargs):
        comments = data.get('comments')
        if comments is not None:
            comments = [Comment.new_from_json_dict(item) for item in comments]
        return super().new_from_json_dict(data=data, comments=comments)


class CommentTread(BaseModel):
    """
    A class representing comment thread info.
    Refer: https://developers.google.com/youtube/v3/docs/commentThreads
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.param_defaults = {
            'kind': None,
            'etag': None,
            'id': None,
            'snippet': None,
            'replies': None,
        }
        self.initial(kwargs)

    def __repr__(self):
        return f"CommentTread(id={self.id},kind={self.kind})"

    @classmethod
    def new_from_json_dict(cls, data, **kwargs):
        snippet = data.get('snippet')
        if snippet is not None:
            snippet = CommentTreadSnippet.new_from_json_dict(snippet)
        replies = data.get('replies')
        if replies is not None:
            replies = CommentTreadReplies.new_from_json_dict(replies)

        return super().new_from_json_dict(
            data=data, snippet=snippet,
            replies=replies
        )
