from __future__ import annotations

from typing import TYPE_CHECKING, List, Tuple

from ..db import execute_read_query

__all__ = (
    "query_ticket",
    "query_ticket_by_channel",
    "query_ticket_by_config",
    "query_ticket_by_guild",
    "query_ticket_config",
    "query_ticket_config_by_category",
    "query_ticket_config_by_guild",
    "query_current_ticket_number",
)

if TYPE_CHECKING:
    from _typings import TicketConfigData, TicketData


async def query_ticket(ticket_id: int) -> TicketData:
    return (
        await execute_read_query("SELECT * FROM tickets WHERE id = $1;", ticket_id)
    )[0]


async def query_ticket_by_channel(channel_id: int) -> TicketData:
    return (
        await execute_read_query(
            "SELECT * FROM tickets WHERE channel_id = $1;", channel_id
        )
    )[0]


async def query_ticket_by_guild(guild_id: int) -> Tuple[TicketData, ...]:
    return tuple(
        await execute_read_query("SELECT * FROM tickets WHERE guild_id = $1;", guild_id)
    )


async def query_ticket_by_config(config_id: int) -> List[TicketData]:
    return await execute_read_query("SELECT * FROM tickets WHERE id = $1;", config_id)


async def query_ticket_config(config_id: int) -> TicketConfigData:
    return (
        await execute_read_query(
            "SELECT * FROM ticket_configs WHERE id = $1;", config_id
        )
    )[0]


async def query_ticket_config_by_category(category_id: int) -> TicketConfigData:
    return (
        await execute_read_query(
            "SELECT * FROM ticket_configs WHERE category_id = $1;", category_id
        )
    )[0]


async def query_ticket_config_by_guild(guild_id: int) -> Tuple[TicketConfigData, ...]:
    return tuple(
        await execute_read_query(
            "SELECT * FROM ticket_configs WHERE guild_id = $1;", guild_id
        )
    )


async def query_current_ticket_number(config_id: int) -> int:
    return (
        await execute_read_query(
            "SELECT MAX(ticket_number) FROM tickets WHERE id = $1;",
            config_id,
        )
    )[0][0]
