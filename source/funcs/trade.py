from ..data.classes import TradePrices
from ..data.get import get_prices


async def get_trade_prices():
    return TradePrices(await get_prices())
