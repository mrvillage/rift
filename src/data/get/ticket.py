from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from ..query import (
    query_current_ticket_number,
    query_ticket,
    query_ticket_by_channel,
    query_ticket_by_config,
    query_ticket_config,
    query_ticket_config_by_category,
)

__all__ = ("get_ticket", "get_ticket_config", "get_current_ticket_number")

if TYPE_CHECKING:
    from _typings import TicketConfigData, TicketData


async def get_ticket(
    *,
    ticket_id: Optional[int] = None,
    channel_id: Optional[int] = None,
    config_id: Optional[int] = None
) -> TicketData:
    if ticket_id is not None:
        return await query_ticket(ticket_id)
    if channel_id is not None:
        return await query_ticket_by_channel(channel_id)
    if config_id is not None:
        return (await query_ticket_by_config(config_id))[0]
    raise ValueError("No arguments given")


async def get_ticket_config(
    *, config_id: Optional[int] = None, category_id: Optional[int] = None
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
