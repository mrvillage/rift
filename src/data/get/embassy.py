from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from ..query import (
    query_embassy,
    query_embassy_by_channel,
    query_embassy_by_config,
    query_embassy_config,
    query_embassy_config_by_category,
)

__all__ = ("get_embassy", "get_embassy_config")

if TYPE_CHECKING:
    from _typings import EmbassyConfigData, EmbassyData


async def get_embassy(
    *,
    embassy_id: Optional[int] = None,
    channel_id: Optional[int] = None,
    config_id: Optional[int] = None
) -> EmbassyData:
    if embassy_id is not None:
        return await query_embassy(embassy_id)
    if channel_id is not None:
        return await query_embassy_by_channel(channel_id)
    if config_id is not None:
        return (await query_embassy_by_config(config_id))[0]
    raise ValueError("No arguments given")


async def get_embassy_config(
    *, config_id: Optional[int] = None, category_id: Optional[int] = None
) -> EmbassyConfigData:
    if config_id is not None:
        return await query_embassy_config(config_id)
    if category_id is not None:
        return await query_embassy_config_by_category(category_id)
    raise ValueError("No arguments given")
