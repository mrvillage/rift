from __future__ import annotations

import json
import sys
import traceback
from asyncio import sleep
from typing import Literal

import aiohttp
from discord.backoff import ExponentialBackoff
from discord.ext import commands

from ... import funcs
from ...env import SOCKET_IP, SOCKET_PORT
from ...ref import Rift


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
                        f"ws://{SOCKET_IP}:{SOCKET_PORT}", max_msg_size=0, timeout=5
                    ) as ws:
                        print("rift-data socket connected", flush=True)
                        async for message in ws:
                            data = message.json()
                            if "event" in data:
                                self.bot.dispatch(data["event"], **data["data"])
            except ConnectionRefusedError:
                print("rift-data socket refused", flush=True)
                delay = backoff.delay()
                await sleep(delay)
            except Exception as error:
                print("rift-data socket connection error", file=sys.stderr, flush=True)
                traceback.print_exception(
                    type(error), error, error.__traceback__, file=sys.stderr
                )
                delay = backoff.delay()
                await sleep(delay)

    @commands.command(
        name="subscribe",
        help="Subscribe to an event stream. Note: Not all types are valid for every event.",
        type=commands.CommandType.chat_input,
    )
    async def subscribe(
        self,
        ctx: commands.Context,
        *,
        event: Literal[
            "ALLIANCE", "COLOR", "FORUM", "PRICE", "NATION"
        ],  # TRADE, TREASURE, WAR
        type: Literal["CREATE", "DELETE", "UPDATE"],  # ACCEPT, VICTORY
    ):
        ...


def setup(bot: Rift):
    bot.add_cog(Events(bot))
