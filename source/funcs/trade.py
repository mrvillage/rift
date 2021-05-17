from ..data.get import get_prices
from ..data.classes import TradePrices


async def get_trade_prices():
    return TradePrices(await get_prices())
