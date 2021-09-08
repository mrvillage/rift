from __future__ import annotations

import json
import sys
import traceback
from asyncio import sleep

import aiohttp
from discord.backoff import ExponentialBackoff
from discord.ext import commands

from ... import funcs
from ...env import SOCKET_IP, SOCKET_PORT
from ...ref import Rift

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
    def __init__(self, bot: Rift):
        self.bot = bot
        self.bot.loop.create_task(self.socket())

    async def socket(self):
        backoff = ExponentialBackoff()
        while True:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.ws_connect(
                        f"ws://{SOCKET_IP}:{SOCKET_PORT}", max_msg_size=0
                    ) as ws:
                        print("rift-data socket connected", flush=True)
                        async for message in ws:
                            data = message.json()
                            if "event" in data:
                                event: str = data["event"]
                                event = EVENTS.get(event, event)
                                self.bot.dispatch(event, **data["data"])
            except Exception as error:
                print("rift-data socket connection error", file=sys.stderr, flush=True)
                traceback.print_exception(
                    type(error), error, error.__traceback__, file=sys.stderr
                )
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


def setup(bot: Rift):
    bot.add_cog(Events(bot))
