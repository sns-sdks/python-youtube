"""
    some constants for YouTube
"""

CHANNEL_RESOURCE_PROPERTIES = {
    "id",
    "brandingSettings",
    "contentDetails",
    "localizations",
    "snippet",
    "statistics",
    "status",
    "topicDetails",
}

CHANNEL_SECTIONS_PROPERTIES = {
    "id",
    "contentDetails",
    "localizations",
    "snippet",
    "targeting",
}

PLAYLIST_RESOURCE_PROPERTIES = {
    "id",
    "contentDetails",
    "localizations",
    "player",
    "snippet",
    "status",
}

PLAYLIST_ITEM_RESOURCE_PROPERTIES = {"id", "contentDetails", "snippet", "status"}

VIDEO_RESOURCE_PROPERTIES = {
    "id",
    "contentDetails",
    "player",
    "snippet",
    "statistics",
    "status",
    "topicDetails",
    "liveStreamingDetails",
}

COMMENT_THREAD_RESOURCE_PROPERTIES = {"id", "replies", "snippet"}

COMMENT_RESOURCE_PROPERTIES = {"id", "snippet"}

VIDEO_CATEGORY_RESOURCE_PROPERTIES = {"id", "snippet"}

GUIDE_CATEGORY_RESOURCE_PROPERTIES = {"id", "snippet"}

SEARCH_RESOURCE_PROPERTIES = {"id", "snippet"}

SUBSCRIPTION_RESOURCE_PROPERTIES = {
    "id",
    "snippet",
    "contentDetails",
    "subscriberSnippet",
}

ACTIVITIES_RESOURCE_PROPERTIES = {
    "id",
    "snippet",
    "contentDetails",
}

CAPTIONS_RESOURCE_PROPERTIES = {
    "id",
    "snippet",
}

I18N_REGION_PROPERTIES = {
    "id",
    "snippet",
}

I18N_LANGUAGE_PROPERTIES = {
    "id",
    "snippet",
}

VIDEO_ABUSE_REPORT_REASON_PROPERTIES = {
    "id",
    "snippet",
}

MEMBER_PROPERTIES = {
    "id",
    "snippet",
}

MEMBERSHIP_LEVEL_PROPERTIES = {
    "id",
    "snippet",
}

RESOURCE_PARTS_MAPPING = {
    "channels": CHANNEL_RESOURCE_PROPERTIES,
    "channelSections": CHANNEL_SECTIONS_PROPERTIES,
    "playlists": PLAYLIST_RESOURCE_PROPERTIES,
    "playlistItems": PLAYLIST_ITEM_RESOURCE_PROPERTIES,
    "videos": VIDEO_RESOURCE_PROPERTIES,
    "commentThreads": COMMENT_THREAD_RESOURCE_PROPERTIES,
    "comments": COMMENT_RESOURCE_PROPERTIES,
    "videoCategories": VIDEO_CATEGORY_RESOURCE_PROPERTIES,
    "guideCategories": GUIDE_CATEGORY_RESOURCE_PROPERTIES,
    "search": SEARCH_RESOURCE_PROPERTIES,
    "subscriptions": SUBSCRIPTION_RESOURCE_PROPERTIES,
    "activities": ACTIVITIES_RESOURCE_PROPERTIES,
    "captions": CAPTIONS_RESOURCE_PROPERTIES,
    "i18nRegions": I18N_REGION_PROPERTIES,
    "i18nLanguages": I18N_LANGUAGE_PROPERTIES,
    "videoAbuseReportReasons": VIDEO_ABUSE_REPORT_REASON_PROPERTIES,
    "members": MEMBER_PROPERTIES,
    "membershipsLevels": MEMBERSHIP_LEVEL_PROPERTIES,
}

TOPICS = {
    # Music topics
    "/m/04rlf": "Music (parent topic)",
    "/m/02mscn": "Christian music",
    "/m/0ggq0m": "Classical music",
    "/m/01lyv": "Country",
    "/m/02lkt": "Electronic music",
    "/m/0glt670": "Hip hop music",
    "/m/05rwpb": "Independent music",
    "/m/03_d0": "Jazz",
    "/m/028sqc": "Music of Asia",
    "/m/0g293": "Music of Latin America",
    "/m/064t9": "Pop music",
    "/m/06cqb": "Reggae",
    "/m/06j6l": "Rhythm and blues",
    "/m/06by7": "Rock music",
    "/m/0gywn": "Soul music",
    # Gaming topics
    "/m/0bzvm2": "Gaming (parent topic)",
    "/m/025zzc": "Action game",
    "/m/02ntfj": "Action-adventure game",
    "/m/0b1vjn": "Casual game",
    "/m/02hygl": "Music video game",
    "/m/04q1x3q": "Puzzle video game",
    "/m/01sjng": "Racing video game",
    "/m/0403l3g": "Role-playing video game",
    "/m/021bp2": "Simulation video game",
    "/m/022dc6": "Sports game",
    "/m/03hf_rm": "Strategy video game",
    # Sports topics
    "/m/06ntj": "Sports (parent topic)",
    "/m/0jm_": "American football",
    "/m/018jz": "Baseball",
    "/m/018w8": "Basketball",
    "/m/01cgz": "Boxing",
    "/m/09xp_": "Cricket",
    "/m/02vx4": "Football",
    "/m/037hz": "Golf",
    "/m/03tmr": "Ice hockey",
    "/m/01h7lh": "Mixed martial arts",
    "/m/0410tth": "Motorsport",
    "/m/07bs0": "Tennis",
    "/m/07_53": "Volleyball",
    # Entertainment topics
    "/m/02jjt": "Entertainment (parent topic)",
    "/m/09kqc": "Humor",
    "/m/02vxn": "Movies",
    "/m/05qjc": "Performing arts",
    "/m/066wd": "Professional wrestling",
    "/m/0f2f9": "TV shows",
    # Lifestyle topics
    "/m/019_rr": "Lifestyle (parent topic)",
    "/m/032tl": "Fashion",
    "/m/027x7n": "Fitness",
    "/m/02wbm": "Food",
    "/m/03glg": "Hobby",
    "/m/068hy": "Pets",
    "/m/041xxh": "Physical attractiveness [Beauty]",
    "/m/07c1v": "Technology",
    "/m/07bxq": "Tourism",
    "/m/07yv9": "Vehicles",
    # Society topics
    "/m/098wr": "Society (parent topic)",
    "/m/09s1f": "Business",
    "/m/0kt51": "Health",
    "/m/01h6rj": "Military",
    "/m/05qt0": "Politics",
    "/m/06bvp": "Religion",
    # Other topics
    "/m/01k8wb": "Knowledge",
}
