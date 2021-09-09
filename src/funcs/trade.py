from __future__ import annotations

import json

from ..data.get import get_prices

__all__ = ("get_trade_prices",)


async def get_trade_prices():
    from ..data.classes import TradePrices

    return TradePrices(
        {  # type: ignore
            key: json.loads(value)
            if key != "datetime" and isinstance(value, str)
            else value
            for key, value in (await get_prices()).items()
        }
    )
