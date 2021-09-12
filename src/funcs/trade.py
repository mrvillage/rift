from __future__ import annotations

from ..cache import cache

__all__ = ("get_trade_prices",)


async def get_trade_prices():
    return cache.prices
