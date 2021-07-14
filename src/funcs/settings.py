async def get_guild_settings(guild_id):
    from ..data.classes import GuildSettings

    settings = await GuildSettings.fetch(guild_id)


async def get_user_settings(user_id):
    from ..data.classes import UserSettings

    settings = await UserSettings.fetch(user_id)
