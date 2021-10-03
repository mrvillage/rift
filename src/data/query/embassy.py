from __future__ import annotations

from typing import TYPE_CHECKING, List, Tuple

from ..db import execute_read_query

__all__ = (
    "query_embassy",
    "query_embassy_by_channel",
    "query_embassy_by_config",
    "query_embassy_by_guild",
    "query_embassy_config",
    "query_embassy_config_by_category",
    "query_embassy_config_by_guild",
)

if TYPE_CHECKING:
    from _typings import EmbassyConfigData, EmbassyData


async def query_embassy(embassy_id: int) -> EmbassyData:
    return (
        await execute_read_query("SELECT * FROM embassies WHERE id = $1;", embassy_id)
    )[0]


async def query_embassy_by_channel(channel_id: int) -> EmbassyData:
    return (
        await execute_read_query(
            "SELECT * FROM embassies WHERE channel_id = $1;", channel_id
        )
    )[0]


async def query_embassy_by_guild(guild_id: int) -> Tuple[EmbassyData, ...]:
    return tuple(
        await execute_read_query(
            "SELECT * FROM embassies WHERE guild_id = $1;", guild_id
        )
    )


async def query_embassy_by_config(config_id: int) -> List[EmbassyData]:
    return await execute_read_query("SELECT * FROM embassies WHERE id = $1;", config_id)


async def query_embassy_config(config_id: int) -> EmbassyConfigData:
    return (
        await execute_read_query(
            "SELECT * FROM embassy_configs WHERE id = $1;", config_id
        )
    )[0]


async def query_embassy_config_by_category(category_id: int) -> EmbassyConfigData:
    return (
        await execute_read_query(
            "SELECT * FROM embassy_configs WHERE category_id = $1;", category_id
        )
    )[0]


async def query_embassy_config_by_guild(guild_id: int) -> Tuple[EmbassyConfigData, ...]:
    return tuple(
        await execute_read_query(
            "SELECT * FROM embassy_configs WHERE guild_id = $1;", guild_id
        )
    )
