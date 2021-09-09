from __future__ import annotations

import datetime

import discord
from discord.ext import commands, tasks

from ...cache import cache
from ...data.db import execute_read_query
from ...ref import Rift


class Cache(commands.Cog):
    def __init__(self, bot: Rift):
        self.bot = bot
        self.verify_cache_integrity.start()

    @commands.Cog.listener()
    async def on_bulk_alliance_created(self, data):
        for i in data:
            cache.hook_alliance("create", i)

    @commands.Cog.listener()
    async def on_bulk_alliance_update(self, data):
        for i in data:
            cache.hook_alliance("update", i["after"])
        if cache.validate.alliances:
            fetched_data = await execute_read_query("SELECT * FROM alliances;")
            for i in (dict(i) for i in fetched_data):
                cache.hook_alliance("update", i)  # type: ignore

    @commands.Cog.listener()
    async def on_bulk_alliance_deleted(self, data):
        for i in data:
            cache.hook_alliance("delete", i)

    @commands.Cog.listener()
    async def on_bulk_city_created(self, data):
        for i in data:
            cache.hook_city("create", i)

    @commands.Cog.listener()
    async def on_bulk_city_update(self, data):
        for i in data:
            cache.hook_city("update", i["after"])
        if cache.validate.cities:
            fetched_data = await execute_read_query("SELECT * FROM cities;")
            for i in (dict(i) for i in fetched_data):
                cache.hook_city("update", i)  # type: ignore

    @commands.Cog.listener()
    async def on_bulk_city_deleted(self, data):
        for i in data:
            cache.hook_city("delete", i)

    @commands.Cog.listener()
    async def on_colors_update(self, before, after):
        for i in after:
            cache.hook_color("update", i)
        if cache.validate.alliances:
            fetched_data = await execute_read_query(
                "SELECT * FROM colors ORDER BY datetime DESC LIMIT 1;"
            )
            for i in (dict(i) for i in fetched_data[0]["colors"]):
                cache.hook_alliance("update", i)  # type: ignore

    @commands.Cog.listener()
    async def on_bulk_nation_created(self, data):
        for i in data:
            cache.hook_nation("create", i)

    @commands.Cog.listener()
    async def on_bulk_nation_update(self, data):
        for i in data:
            cache.hook_nation("update", i["after"])
        if cache.validate.nations:
            fetched_data = await execute_read_query("SELECT * FROM nations;")
            for i in (dict(i) for i in fetched_data):
                cache.hook_nation("update", i)  # type: ignore

    @commands.Cog.listener()
    async def on_bulk_nation_deleted(self, data):
        for i in data:
            cache.hook_nation("delete", i)

    @commands.Cog.listener()
    async def on_prices_update(self, before, after):
        for i in after:
            cache.hook_price("update", i)
        if cache.validate.prices:
            fetched_data = await execute_read_query(
                "SELECT * FROM prices ORDER BY datetime DESC LIMIT 1;"
            )
            cache.hook_price("update", fetched_data[0])  # type: ignore

    @commands.Cog.listener()
    async def on_bulk_new_treaty(self, data):
        for i in data:
            cache.hook_treaty("create", i)
        if cache.validate.treaties:
            fetched_data = await execute_read_query("SELECT * FROM treaties;")
            for i in (dict(i) for i in fetched_data):
                cache.hook_city("update", i)  # type: ignore

    @commands.Cog.listener()
    async def on_bulk_treaty_expired(self, data):
        for i in data:
            cache.hook_treaty("delete", i)

    @tasks.loop(hours=1)
    async def verify_cache_integrity(self):
        for key in cache.validate.__dict__.keys():
            setattr(cache.validate, key, True)

    @verify_cache_integrity.before_loop
    async def before_verify_cache_integrity(self):
        await self.bot.wait_until_ready()
        now = datetime.datetime.utcnow()
        wait = now.replace(minute=59, second=45)
        while wait < now:
            wait += datetime.timedelta(hours=1)
        await discord.utils.sleep_until(wait)


def setup(bot: Rift):
    bot.add_cog(Cache(bot))
