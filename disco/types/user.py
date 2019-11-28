from datetime import datetime

from disco.types.base import (
    SlottedModel, Field, snowflake, text, with_equality, with_hash, enum, ListField,
    cached_property,
)


class DefaultAvatars(object):
    BLURPLE = 0
    GREY = 1
    GREEN = 2
    ORANGE = 3
    RED = 4

    ALL = [BLURPLE, GREY, GREEN, ORANGE, RED]


class UserFlags(object):
    NONE = 0
    DISCORD_EMPLOYEE = 1 << 0
    DISCORD_PARTNER = 1 << 1
    HS_EVENTS = 1 << 2
    BUG_HUNTER = 1 << 3
    HS_BRAVERY = 1 << 6
    HS_BRILLIANCE = 1 << 7
    HS_BALANCE = 1 << 8
    EARLY_SUPPORTER = 1 << 9
    TEAM_USER = 1 << 10


class PremiumType(object):
    CLASSIC = 1
    NITRO = 2


class User(SlottedModel, with_equality('id'), with_hash('id')):
    id = Field(snowflake)
    username = Field(text)
    discriminator = Field(text)
    avatar = Field(text)
    bot = Field(bool, default=False)
    mfa_enabled = Field(bool)
    locale = Field(text)
    verified = Field(bool)
    email = Field(text)
    flags = Field(int)
    premium_type = Field(int)

    presence = Field(None)

    def get_avatar_url(self, still_format='webp', animated_format='gif', size=1024):
        if not self.avatar:
            return 'https://cdn.discordapp.com/embed/avatars/{}.png'.format(self.default_avatar)

        if self.avatar.startswith('a_'):
            return 'https://cdn.discordapp.com/avatars/{}/{}.{}?size={}'.format(
                self.id, self.avatar, animated_format, size
            )
        else:
            return 'https://cdn.discordapp.com/avatars/{}/{}.{}?size={}'.format(
                self.id, self.avatar, still_format, size
            )

    @property
    def default_avatar(self):
        return DefaultAvatars.ALL[int(self.discriminator) % len(DefaultAvatars.ALL)]

    @property
    def avatar_url(self):
        return self.get_avatar_url()

    @property
    def mention(self):
        return '<@{}>'.format(self.id)

    def open_dm(self):
        return self.client.api.users_me_dms_create(self.id)

    def __str__(self):
        return u'{}#{}'.format(self.username, str(self.discriminator).zfill(4))

    def __repr__(self):
        return u'<User {} ({})>'.format(self.id, self)


class ClientStatus(object):
    DESKTOP = 'DESKTOP'
    MOBILE = 'MOBILE'
    WEB = 'WEB'


class ActivityType(object):
    DEFAULT = 0
    STREAMING = 1
    LISTENING = 2
    WATCHING = 3
    CUSTOM = 4


class ActivityEmoji(SlottedModel):
    name = Field(text)
    id = Field(int)
    animated = Field(bool)


class Status(object):
    ONLINE = 'ONLINE'
    IDLE = 'IDLE'
    DND = 'DND'
    INVISIBLE = 'INVISIBLE'
    OFFLINE = 'OFFLINE'


class Party(SlottedModel):
    id = Field(text)
    size = ListField(int)


class Assets(SlottedModel):
    large_image = Field(text)
    large_text = Field(text)
    small_image = Field(text)
    small_text = Field(text)


class Secrets(SlottedModel):
    join = Field(text)
    spectate = Field(text)
    match = Field(text)


class Timestamps(SlottedModel):
    start = Field(int)
    end = Field(int)

    @cached_property
    def start_time(self):
        return datetime.utcfromtimestamp(self.start / 1000)

    @cached_property
    def end_time(self):
        return datetime.utcfromtimestamp(self.end / 1000)

class Activity(SlottedModel):
    name = Field(text)
    type = Field(enum(ActivityType))
    url = Field(text)
    timestamps = Field(Timestamps)
    application_id = Field(text)
    details = Field(text)
    state = Field(text)
    emoji = Field(ActivityEmoji)
    party = Field(Party)
    assets = Field(Assets)
    secrets = Field(Secrets)
    instance = Field(bool)
    flags = Field(int)


class Presence(SlottedModel):
    user = Field(User, alias='user', ignore_dump=['presence'])
    game = Field(Activity)
    status = Field(enum(Status))
    client_status = Field(enum(ClientStatus))
