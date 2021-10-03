from __future__ import annotations

from typing import TYPE_CHECKING, Union

from ..db import execute_read_query

__all__ = ("get_guild_settings", "get_guild_welcome_settings")

if TYPE_CHECKING:
    from _typings import GuildSettingsData, GuildWelcomeSettingsData


async def get_guild_settings(guild_id: int) -> Union[GuildSettingsData, None]:
    data = await execute_read_query(
        "SELECT * FROM guild_settings WHERE guild_id = $1;", guild_id
    )
    return data[0] if data else None


async def get_guild_welcome_settings(
    guild_id: int,
) -> Union[GuildWelcomeSettingsData, None]:
    data = await execute_read_query(
        "SELECT * FROM guild_welcome_settings WHERE guild_id = $1;", guild_id
    )
    return data[0] if data else None
