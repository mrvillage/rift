from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Union

from src.data.query.ticket import (
    query_current_ticket_number,
    query_ticket,
    query_ticket_config,
    query_ticket_config_by_category,
)

from ..query import (
    query_ticket,
    query_ticket_by_channel,
    query_ticket_by_config,
    query_ticket_by_guild,
)

__all__ = ("get_ticket", "get_ticket_config", "get_current_ticket_number")

if TYPE_CHECKING:
    from typings import TicketConfigData, TicketData


async def get_ticket(
    *,
    ticket_id: int = None,
    channel_id: int = None,
    config_id: int = None,
    guild_id: int = None
) -> TicketData:
    if ticket_id is not None:
        return await query_ticket(ticket_id)
    if channel_id is not None:
        return await query_ticket_by_channel(channel_id)
    if config_id is not None:
        return await query_ticket_by_config(config_id)
    if guild_id is not None:
        return await query_ticket_by_guild(guild_id)
    raise ValueError("No arguments given")


async def get_ticket_config(
    *, config_id: int = None, category_id: int = None
) -> TicketConfigData:
    if config_id is not None:
        return await query_ticket_config(config_id)
    if category_id is not None:
        return await query_ticket_config_by_category(category_id)
    raise ValueError("No arguments given")


async def get_current_ticket_number(config_id: int) -> int:
    data = await query_current_ticket_number(config_id)
    if data is None:
        return 0
    return data
