from __future__ import annotations

from typing import Union

from ..db import execute_read_query


async def get_guild_settings(guild_id: int) -> Union[tuple, None]:
    data = await execute_read_query(
        "SELECT * FROM guild_settings WHERE guild_id = $1;", guild_id
    )
    return tuple(data[0]) if data else None


async def get_guild_welcome_settings(guild_id: int) -> Union[tuple, None]:
    data = await execute_read_query(
        "SELECT * FROM guild_welcome_settings WHERE guild_id = $1;", guild_id
    )
    return tuple(data[0]) if data else None
