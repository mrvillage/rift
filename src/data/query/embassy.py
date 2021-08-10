from __future__ import annotations

from typing import TYPE_CHECKING, Tuple

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
    from typings import EmbassyConfigData, EmbassyData


async def query_embassy(embassy_id: int) -> EmbassyData:
    data = dict(
        (
            await execute_read_query(
                "SELECT * FROM embassies WHERE embassy_id = $1;", embassy_id
            )
        )[0]
    )
    if TYPE_CHECKING:
        assert isinstance(data, EmbassyData)
    return data


async def query_embassy_by_channel(channel_id: int) -> EmbassyData:
    data = dict(
        (
            await execute_read_query(
                "SELECT * FROM embassies WHERE channel_id = $1;", channel_id
            )
        )[0]
    )
    if TYPE_CHECKING:
        assert isinstance(data, EmbassyData)
    return data


async def query_embassy_by_guild(guild_id: int) -> Tuple[EmbassyData, ...]:
    raw = await execute_read_query(
        "SELECT * FROM embassies WHERE guild_id = $1;", guild_id
    )
    data = []
    for dat in raw:
        if TYPE_CHECKING:
            assert isinstance(data, EmbassyData)
        data.append(dat)
    return tuple(data)


async def query_embassy_by_config(config_id: int) -> EmbassyData:
    data = dict(
        (
            await execute_read_query(
                "SELECT * FROM embassies WHERE config_id = $1;", config_id
            )
        )
    )
    if TYPE_CHECKING:
        assert isinstance(data, EmbassyData)
    return data


async def query_embassy_config(config_id: int) -> EmbassyConfigData:
    data = dict(
        (
            await execute_read_query(
                "SELECT * FROM embassy_configs WHERE config_id = $1;", config_id
            )
        )[0]
    )
    if TYPE_CHECKING:
        assert isinstance(data, EmbassyConfigData)
    return data


async def query_embassy_config_by_category(category_id: int) -> EmbassyConfigData:
    data = dict(
        (
            await execute_read_query(
                "SELECT * FROM embassy_configs WHERE category_id = $1;", category_id
            )
        )[0]
    )
    if TYPE_CHECKING:
        assert isinstance(data, EmbassyConfigData)
    return data


async def query_embassy_config_by_guild(guild_id: int) -> Tuple[EmbassyConfigData, ...]:
    raw = await execute_read_query(
        "SELECT * FROM embassy_configs WHERE guild_id = $1;", guild_id
    )
    data = []
    for dat in raw:
        if TYPE_CHECKING:
            assert isinstance(data, EmbassyConfigData)
        data.append(dat)
    return tuple(data)
