from __future__ import annotations

from typing import TYPE_CHECKING

from ..query import (
    query_embassy,
    query_embassy_by_channel,
    query_embassy_by_config,
    query_embassy_by_guild,
    query_embassy_config,
    query_embassy_config_by_category,
)

__all__ = ("get_embassy", "get_embassy_config")

if TYPE_CHECKING:
    from typings import EmbassyConfigData, EmbassyData


async def get_embassy(
    *, embassy_id: int = None, channel_id: int = None, config_id: int = None
) -> EmbassyData:
    if embassy_id is not None:
        return await query_embassy(embassy_id)
    if channel_id is not None:
        return await query_embassy_by_channel(channel_id)
    if config_id is not None:
        return await query_embassy_by_config(config_id)
    raise ValueError("No arguments given")


async def get_embassy_config(
    *, config_id: int = None, category_id: int = None
) -> EmbassyConfigData:
    if config_id is not None:
        return await query_embassy_config(config_id)
    if category_id is not None:
        return await query_embassy_config_by_category(category_id)
    raise ValueError("No arguments given")
