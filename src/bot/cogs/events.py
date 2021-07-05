import json
import aiohttp
from discord.ext import commands

from ... import funcs as rift
from ...env import SOCKET_PORT, SOCKET_IP

EVENTS = {
    "alliance_update": "raw_alliance_update",
    "city_update": "raw_city_update",
    "market_prices_update": "raw_market_prices_update",
    "nation_update": "raw_nation_update",
    "pending_trade_update": "raw_pending_trade_update",
    "prices_update": "raw_prices_update",
    "treasures_update": "raw_treasures_update",
    "war_update": "raw_war_update",
}


class Events(commands.Cog):
    def __init__(self, bot: rift.Rift):
        self.bot = bot
        self.bot.loop.create_task(self.socket())

    async def socket(self):
        async with aiohttp.ClientSession() as session:
            async with session.ws_connect(f"wss://{SOCKET_IP}:{SOCKET_PORT}") as ws:
                async for message in ws:
                    data: dict[str, str, dict] = json.loads(message.data)
                    if "event" in data:
                        event: str = data["event"]
                        event = EVENTS.get(event, default=event)
                        self.bot.dispatch(data["event"], **data["data"])


def setup(bot: rift.Rift):
    bot.add_cog(Events(bot))
