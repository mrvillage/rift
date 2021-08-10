from __future__ import annotations

from typing import TYPE_CHECKING, Tuple

from ..db import execute_read_query

__all__ = (
    "query_ticket",
    "query_ticket_by_channel",
    "query_ticket_by_config",
    "query_ticket_by_guild",
    "query_ticket_config",
    "query_ticket_config_by_guild",
    "query_current_ticket_number",
)

if TYPE_CHECKING:
    from typings import TicketConfigData, TicketData


async def query_ticket(ticket_id: int) -> TicketData:
    data = dict(
        (
            await execute_read_query(
                "SELECT * FROM tickets WHERE ticket_id = $1;", ticket_id
            )
        )[0]
    )
    if TYPE_CHECKING:
        assert isinstance(data, TicketData)
    return data


async def query_ticket_by_channel(channel_id: int) -> TicketData:
    data = dict(
        (
            await execute_read_query(
                "SELECT * FROM tickets WHERE channel_id = $1;", channel_id
            )
        )[0]
    )
    if TYPE_CHECKING:
        assert isinstance(data, TicketData)
    return data


async def query_ticket_by_guild(guild_id: int) -> TicketData:
    data = dict(
        (
            await execute_read_query(
                "SELECT * FROM tickets WHERE guild_id = $1;", guild_id
            )
        )
    )
    if TYPE_CHECKING:
        assert isinstance(data, TicketData)
    return data


async def query_ticket_by_config(config_id: int) -> TicketData:
    data = dict(
        (
            await execute_read_query(
                "SELECT * FROM tickets WHERE config_id = $1;", config_id
            )
        )
    )
    if TYPE_CHECKING:
        assert isinstance(data, TicketData)
    return data


async def query_ticket_config(config_id: int) -> TicketConfigData:
    data = dict(
        (
            await execute_read_query(
                "SELECT * FROM ticket_configs WHERE config_id = $1;", config_id
            )
        )[0]
    )
    if TYPE_CHECKING:
        assert isinstance(data, TicketConfigData)
    return data


async def query_ticket_config_by_category(category_id: int) -> TicketConfigData:
    data = dict(
        (
            await execute_read_query(
                "SELECT * FROM ticket_configs WHERE category_id = $1;", category_id
            )
        )[0]
    )
    if TYPE_CHECKING:
        assert isinstance(data, TicketConfigData)
    return data


async def query_ticket_config_by_guild(guild_id: int) -> Tuple[TicketConfigData, ...]:
    raw = await execute_read_query(
        "SELECT * FROM ticket_configs WHERE guild_id = $1;", guild_id
    )
    data = []
    for dat in raw:
        if TYPE_CHECKING:
            assert isinstance(data, TicketConfigData)
        data.append(dat)
    return tuple(data)


async def query_current_ticket_number(config_id: int) -> int:
    data = (
        await execute_read_query(
            "SELECT MAX(ticket_number) FROM tickets WHERE config_id = $1;",
            config_id,
        )
    )[0][0]
    if TYPE_CHECKING:
        assert isinstance(data, int)
    return data
