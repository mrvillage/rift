from __future__ import annotations

from typing import TYPE_CHECKING

from ..db import execute_read_query

__all__ = ("get_prices",)

if TYPE_CHECKING:
    from _typings import TradePriceData


async def get_prices() -> TradePriceData:
    return (
        await execute_read_query("SELECT * FROM prices ORDER BY datetime DESC LIMIT 1;")
    )[0]
