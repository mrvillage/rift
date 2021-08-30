import json
import ssl
import aiohttp
from asyncio import sleep
from discord import backoff
from discord.backoff import ExponentialBackoff
from discord.ext import commands

from ... import funcs
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
    def __init__(self, bot: funcs.Rift):
        self.bot = bot
        self.bot.loop.create_task(self.socket())

    async def socket(self):
        backoff = ExponentialBackoff()
        while True:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.ws_connect(
                        f"ws://{SOCKET_IP}:{SOCKET_PORT}",
                        # ssl=ssl.create_default_context(ssl.Purpose.CLIENT_AUTH),
                    ) as ws:
                        print("rift-data socket connected")
                        async for message in ws:
                            data = json.loads(message.data)
                            if "event" in data:
                                event: str = data["event"]
                                event = EVENTS.get(event, event)
                                # print(event, data if "created" in event else None)
                                self.bot.dispatch(event, **data["data"])
            except Exception:
                print("rift-data socket connection error")
                delay = backoff.delay()
                await sleep(delay)

    @commands.command(
        name="subscribe", help="Subscribe to an event stream.", enabled=False
    )
    async def subscribe(self, ctx: commands.Context, *, event: str):
        if event not in self.bot.subscribable_events:
            await ctx.send(f"{event} is not a valid event.")
            return
        await ctx.send(f"{event} successfully subscribed.")


def setup(bot: funcs.Rift):
    bot.add_cog(Events(bot))
