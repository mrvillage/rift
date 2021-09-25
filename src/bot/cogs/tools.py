from __future__ import annotations

import discord
import pnwkit
from discord.ext import commands

from ... import Rift, funcs
from ...data.classes import Nation
from ...ref import Rift


class Tools(commands.Cog):
    def __init__(self, bot: Rift):
        self.bot = bot

    @commands.group(name="tools", type=commands.CommandType.chat_input)
    async def tools(self, ctx: commands.Context):
        ...

    @tools.command(name="infrastructure", type=commands.CommandType.chat_input)
    async def tools_infrastructure(
        self,
        ctx: commands.Context,
        *,
        before: float,
        after: float,
        urbanization_policy: bool = False,
        center_for_civil_engineering: bool = False,
        advanced_engineering_corps: bool = False,
    ):
        if after - before >= 1000000:
            return await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    "Sorry, but I can't calculate that much infrastructure!",
                    color=discord.Color.red(),
                )
            )
        raw_cost = cost = funcs.calculate_infrastructure_value(before, after)
        if urbanization_policy:
            cost -= raw_cost * 0.05
        if center_for_civil_engineering:
            cost -= raw_cost * 0.05
        if advanced_engineering_corps:
            cost -= raw_cost * 0.05
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"The cost to buy from {before:,.2f} to {after:,.2f} infrastructure is ${cost:,.2f}.",
                color=discord.Color.green(),
            )
        )

    @tools.command(name="land", type=commands.CommandType.chat_input)
    async def tools_land(
        self,
        ctx: commands.Context,
        *,
        before: float,
        after: float,
        rapid_expansion_policy: bool = False,
        arable_land_agency: bool = False,
        advanced_engineering_corps: bool = False,
    ):
        if after - before >= 1000000:
            return await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    "Sorry, but I can't calculate that much land!",
                    color=discord.Color.red(),
                )
            )
        raw_cost = cost = funcs.calculate_land_value(before, after)
        if rapid_expansion_policy:
            cost -= raw_cost * 0.05
        if arable_land_agency:
            cost -= raw_cost * 0.05
        if advanced_engineering_corps:
            cost -= raw_cost * 0.05
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"The cost to buy from {before:,.2f} to {after:,.2f} land is ${cost:,.2f}.",
                color=discord.Color.green(),
            )
        )

    @tools.command(name="city", type=commands.CommandType.chat_input)
    async def tools_city(
        self,
        ctx: commands.Context,
        *,
        before: int,
        after: int,
        manifest_destiny_policy: bool = False,
        urban_planning: bool = False,
        advanced_urban_planning: bool = False,
    ):
        if before < 1 or after > 100:
            return await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    "Sorry, but I can't calculate that range of cities! I can calculate from 1-100.",
                    color=discord.Color.red(),
                )
            )
        raw_cost = cost = funcs.calculate_city_value(before, after)
        if urban_planning:
            cost -= 50000000 * (after - before)
        if advanced_urban_planning:
            cost -= 100000000 * (after - before)
        if manifest_destiny_policy:
            cost -= raw_cost * 0.05
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"The cost to buy from city {before} to city {after} is ${cost:,.2f}.",
                color=discord.Color.green(),
            )
        )

    @tools.group(name="nation", type=commands.CommandType.chat_input)
    async def tools_nation(self, ctx: commands.Context):
        ...

    @tools_nation.command(name="infrastructure", type=commands.CommandType.chat_input)
    async def tools_nation_infrastructure(
        self, ctx: commands.Context, *, nation: Nation, after: float
    ):
        if any(after - i.infrastructure >= 1000000 for i in nation.partial_cities):
            return await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    "Sorry, but I can't calculate that much infrastructure!",
                    color=discord.Color.red(),
                )
            )
        raw_cost = cost = sum(
            funcs.calculate_infrastructure_value(i.infrastructure, after)
            for i in nation.partial_cities
        )
        projects = (
            await pnwkit.async_nation_query(
                {"id": nation.id}, "cfce", "adv_engineering_corps"
            )
        )[0]
        if nation.domestic_policy == "Urbanization":
            cost -= raw_cost * 0.05
        if projects.cfce:
            cost -= raw_cost * 0.05
        if projects.adv_engineering_corps:
            cost -= raw_cost * 0.05
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"The cost to buy all cities of {repr(nation)} to {after:,.2f} infrastructure is ${cost:,.2f}.",
                color=discord.Color.green(),
            )
        )

    @tools_nation.command(name="land", type=commands.CommandType.chat_input)
    async def tools_nation_land(
        self, ctx: commands.Context, *, nation: Nation, after: float
    ):
        if any(after - i.land >= 1000000 for i in nation.partial_cities):
            return await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    "Sorry, but I can't calculate that much land!",
                    color=discord.Color.red(),
                )
            )
        raw_cost = cost = sum(
            funcs.calculate_infrastructure_value(i.infrastructure, after)
            for i in nation.partial_cities
        )
        projects = (
            await pnwkit.async_nation_query(
                {"id": nation.id}, "arable_land_agency", "adv_engineering_corps"
            )
        )[0]
        if nation.domestic_policy == "Rapid Expansion":
            cost -= raw_cost * 0.05
        if projects.arable_land_agency:
            cost -= raw_cost * 0.05
        if projects.adv_engineering_corps:
            cost -= raw_cost * 0.05
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"The cost to buy all cities of {repr(nation)} to {after:,.2f} land is ${cost:,.2f}.",
                color=discord.Color.green(),
            )
        )

    @tools_nation.command(name="city", type=commands.CommandType.chat_input)
    async def tools_nation_city(
        self, ctx: commands.Context, *, nation: Nation, after: int
    ):
        if after > 100:
            return await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    "Sorry, but I can't calculate that range of cities! I can calculate from 1-100.",
                    color=discord.Color.red(),
                )
            )
        raw_cost = cost = funcs.calculate_city_value(nation.cities, after)
        projects = (
            await pnwkit.async_nation_query(
                {"id": nation.id}, "uap", "adv_city_planning"
            )
        )[0]
        if projects.uap:
            cost -= 50000000 * (after - nation.cities)
        if projects.adv_city_planning:
            cost -= 100000000 * (after - nation.cities)
        if nation.domestic_policy == "Manifest Destiny":
            cost -= raw_cost * 0.05
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"The cost to buy {repr(nation)} to city {after} is ${cost:,.2f}.",
                color=discord.Color.green(),
            )
        )


def setup(bot: Rift):
    bot.add_cog(Tools(bot))
