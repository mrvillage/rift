import discord
import asyncio
import json
import aiohttp
import time
import datetime
from discord.ext import commands, tasks
from ... import funcs as rift  # pylint: disable=relative-beyond-top-level
from ... import jobs  # pylint: disable=relative-beyond-top-level
from ...data import cache  # pylint: disable=relative-beyond-top-level
from ...jobs import api  # pylint: disable=relative-beyond-top-level
from ... import jobs  # pylint: disable=relative-beyond-top-level
BASEURL = "https://politicsandwar.com/api"


class Loop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.pnw_session_refresh.start()  # pylint: disable=no-member
        self.fetch_nations.start()  # pylint: disable=no-member
        self.fetch_alliances.start()  # pylint: disable=no-member
        self.fetch_cities.start()  # pylint: disable=no-member

    @tasks.loop(minutes=10)
    async def pnw_session_refresh(self):
        await self.bot.update_pnw_session()

    @tasks.loop(minutes=15)
    async def fetch_nations(self):
        await jobs.target_check()
        await api.fetch_nations()

    @tasks.loop(minutes=15)
    async def fetch_alliances(self):
        await api.fetch_alliances()

    @tasks.loop(minutes=15)
    async def fetch_cities(self):
        await api.fetch_cities()

    @pnw_session_refresh.before_loop
    async def pnw_session_refresh_wait(self):
        now = datetime.datetime.utcnow()
        wait = now.replace(minute=3, second=0)
        while wait < now:
            wait += datetime.timedelta(minutes=10)
        # wait = now
        await discord.utils.sleep_until(wait)

    @fetch_nations.before_loop
    async def fetch_nations_wait(self):
        now = datetime.datetime.utcnow()
        wait = now.replace(minute=5, second=0)
        while wait < now:
            wait += datetime.timedelta(minutes=15)
        print("wait", wait)
        # wait = now
        await discord.utils.sleep_until(wait)

    @fetch_alliances.before_loop
    async def fetch_alliances_wait(self):
        now = datetime.datetime.utcnow()
        wait = now.replace(minute=5, second=0)
        while wait < now:
            wait += datetime.timedelta(minutes=15)
        # wait = now
        await discord.utils.sleep_until(wait)

    @fetch_cities.before_loop
    async def fetch_cities_wait(self):
        now = datetime.datetime.utcnow()
        wait = now.replace(minute=5, second=0)
        while wait < now:
            wait += datetime.timedelta(minutes=15)
        # wait = now
        await discord.utils.sleep_until(wait)


def setup(bot):
    bot.add_cog(Loop(bot))
