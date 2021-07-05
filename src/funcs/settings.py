from ..data.classes import GuildSettings, UserSettings


async def get_guild_settings(guild_id):
    settings = await GuildSettings.fetch(guild_id)


async def get_user_settings(user_id):
    settings = await UserSettings.fetch(user_id)
