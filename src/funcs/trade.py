from ..data.get import get_prices


async def get_trade_prices():
    from ..data.classes import TradePrices

    return TradePrices(await get_prices())
