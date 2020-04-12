from disco.types.base import (
    SlottedModel, Field, ListField, AutoDictField, DictField, snowflake, text, enum, datetime,
    cached_property,
)
from disco.types.user import User

class Account(SlottedModel):
    id = Field(text)
    name = Field(text)


class Integrations(SlottedModel):
    """
    An Integration object.

    Attributes
    ----------
    id : snowflake
        The integration ID.
    name : str
        The integration name.
    type : str
        The integration type (twitch, youtube, etc).
    enabled: bool
        Whether or not the integration is enabled.
    syncing : bool
         Whether or not the integration is syncing.
    role_id : snowflake
        The role .
    enable_emoticons : bool
        The current number of times the invite was used.
    expire_behavior : bool
        Whether this invite only grants temporary membership.
    expire_grace_period : datetime
        Grace period (in days) before expiring subscribers
    user : :Class: <disco.types.user.User>
        The user whose integration this is.
    account : :Class: <disco.types.integrations.Account>
        Information about the account for the integration. 
    synced_at : datetime
        When this integration was last synced.
    """
    id = Field(snowflake)
    name = Field(text)
    type = Field(text)
    enabled = Field(bool)
    syncing = Field(bool)
    role_id = Field(snowflake)
    enable_emoticons = Field(bool)
    expire_behavior = Field(int)
    expire_grace_period = Field(int)
    user = Field(User)
    account = Field(Account)
    synced_at = Field(datetime)
    guild_id = Field(snowflake)

    @cached_property
    def guild(self):
        return self.client.state.guilds.get(self.guild_id)
    
    @cached_property
    def role(self):
        return self.guild.roles.get(self.role_id)
