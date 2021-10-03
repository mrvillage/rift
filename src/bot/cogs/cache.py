from __future__ import annotations

import datetime
import json
from typing import TYPE_CHECKING

import discord
from discord.ext import commands, tasks

from ...cache import cache
from ...data.classes import Alliance, City, Color, Nation, TradePrices, War
from ...data.db import execute_read_query
from ...ref import Rift

if TYPE_CHECKING:
    from typing import List

    from _typings import (
        AllianceData,
        BulkAllianceListData,
        BulkAllianceUpdateData,
        BulkCityListData,
        BulkCityUpdateData,
        BulkNationListData,
        BulkNationUpdateData,
        BulkTreatyListData,
        BulkWarListData,
        CityData,
        ColorUpdateData,
        NationData,
        RawColorData,
        TradePriceData,
        TreatyData,
    )


class Cache(commands.Cog):
    def __init__(self, bot: Rift):
        self.bot = bot
        self.verify_cache_integrity.start()

    @commands.Cog.listener()
    async def on_bulk_alliance_create(self, data: BulkAllianceListData):
        for i in data:
            cache.hook_alliance("create", i)
        for i in data:
            self.bot.dispatch("alliance_create", alliance=cache.get_alliance(i["id"]))

    @commands.Cog.listener()
    async def on_bulk_alliance_update(self, data: BulkAllianceUpdateData):
        for i in data:
            cache.hook_alliance("update", i["after"])
        for i in data:
            self.bot.dispatch(
                "alliance_update",
                before=Alliance(i["before"]),
                after=cache.get_alliance(i["after"]["id"]),
            )
        if cache.validate.alliances:
            fetched_data: List[AllianceData] = await execute_read_query(
                "SELECT * FROM alliances;"
            )
            for i in (dict(i) for i in fetched_data):
                cache.hook_alliance("update", i)  # type: ignore

    @commands.Cog.listener()
    async def on_bulk_alliance_delete(self, data: BulkAllianceListData):
        deleted = {
            i.id: i
            for i in (cache.get_alliance(j["id"]) for j in data)
            if i is not None
        }
        for i in data:
            cache.hook_alliance("delete", i)
        for i in data:
            self.bot.dispatch("alliance_delete", alliance=deleted[i["id"]])

    @commands.Cog.listener()
    async def on_bulk_city_create(self, data: BulkCityListData):
        for i in data:
            cache.hook_city("create", i)
        for i in data:
            self.bot.dispatch("city_create", city=cache.get_city(i["id"]))

    @commands.Cog.listener()
    async def on_bulk_city_update(self, data: BulkCityUpdateData):
        for i in data:
            cache.hook_city("update", i["after"])
        if cache.validate.cities:
            fetched_data: List[CityData] = await execute_read_query(
                "SELECT * FROM cities;"
            )
            for i in (dict(i) for i in fetched_data):
                cache.hook_city("update", i)  # type: ignore
        for i in data:
            self.bot.dispatch(
                "city_update",
                before=City(i["before"]),
                after=cache.get_city(i["after"]["id"]),
            )

    @commands.Cog.listener()
    async def on_bulk_city_delete(self, data: BulkCityListData):
        deleted = {
            i.id: i for i in (cache.get_city(j["id"]) for j in data) if i is not None
        }
        for i in data:
            cache.hook_city("delete", i)
        for i in data:
            self.bot.dispatch("city_delete", city=deleted[i["id"]])

    @commands.Cog.listener()
    async def on_colors_update(self, before: ColorUpdateData, after: ColorUpdateData):
        for i in after:
            cache.hook_color("update", i)
        for i, j in zip(before, after):
            self.bot.dispatch(
                "color_update",
                before=Color(i),
                after=cache.get_color(j["color"]),
            )
        if cache.validate.alliances:
            fetched_data: List[RawColorData] = await execute_read_query(
                "SELECT * FROM colors ORDER BY datetime DESC LIMIT 1;"
            )
            for i in fetched_data[0]["colors"]:
                cache.hook_color("update", i)

    @commands.Cog.listener()
    async def on_bulk_nation_create(self, data: BulkNationListData):
        for i in data:
            cache.hook_nation("create", i)
        for i in data:
            self.bot.dispatch("nation_create", nation=cache.get_nation(i["id"]))

    @commands.Cog.listener()
    async def on_bulk_nation_update(self, data: BulkNationUpdateData):
        for i in data:
            cache.hook_nation("update", i["after"])
        if cache.validate.nations:
            fetched_data: List[NationData] = await execute_read_query(
                "SELECT * FROM nations;"
            )
            for i in fetched_data:
                cache.hook_nation("update", i)  # type: ignore
        for i in data:
            self.bot.dispatch(
                "nation_update",
                before=Nation(i["before"]),
                after=cache.get_nation(i["after"]["id"]),
            )

    @commands.Cog.listener()
    async def on_bulk_nation_delete(self, data: BulkNationListData):
        deleted = {
            i.id: i for i in (cache.get_nation(j["id"]) for j in data) if i is not None
        }
        for i in data:
            cache.hook_nation("delete", i)
        for i in data:
            self.bot.dispatch("nation_delete", nation=deleted[i["id"]])

    @commands.Cog.listener()
    async def on_prices_update(self, before: TradePriceData, after: TradePriceData):
        before = {
            key: json.loads(value) if isinstance(value, str) else value for key, value in before.items()  # type: ignore
        }
        after = {key: json.loads(value) if isinstance(value, str) else value for key, value in after.items()}  # type: ignore
        cache.hook_price("update", after)
        self.bot.dispatch(
            "price_update",
            before=TradePrices(before),
            after=cache.get_prices(),
        )
        if cache.validate.prices:
            fetched_data: List[TradePriceData] = await execute_read_query(
                "SELECT * FROM prices ORDER BY datetime DESC LIMIT 1;"
            )
            cache.hook_price("update", {key: json.loads(value) if isinstance(value, str) and key != "datetime" else value for key, value in dict(fetched_data[0]).items()})  # type: ignore

    @commands.Cog.listener()
    async def on_bulk_treaty_create(self, data: BulkTreatyListData):
        for i in data:
            cache.hook_treaty("create", i)
        for i in data:
            self.bot.dispatch(
                "treaty_create",
                treaty=cache.get_treaty(i["from_"], i["to_"], i["treaty_type"]),
            )
        if cache.validate.treaties:
            fetched_data: List[TreatyData] = await execute_read_query(
                "SELECT * FROM treaties;"
            )
            for i in fetched_data:
                cache.hook_treaty("update", i)  # type: ignore

    @commands.Cog.listener()
    async def on_bulk_treaty_delete(self, data: BulkTreatyListData):
        for i in data:
            cache.hook_treaty("delete", i)
        for i in data:
            self.bot.dispatch(
                "treaty_delete",
                treaty=cache.get_treaty(i["from_"], i["to_"], i["treaty_type"]),
            )

    @commands.Cog.listener()
    async def on_bulk_war_create(self, data: BulkWarListData):
        for i in data:
            self.bot.dispatch("war_create", alliance=War(i))

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
