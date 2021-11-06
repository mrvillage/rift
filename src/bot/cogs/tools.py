from __future__ import annotations

import discord
import pnwkit
from discord.ext import commands
from discord.utils import MISSING

from src.data.classes.alliance import Alliance

from ... import Rift, funcs
from ...data.classes import Nation
from ...ref import Rift, RiftContext


def check_after(before: float, after: float, only_buy: bool) -> bool:
    if only_buy:
        return after > before
    else:
        return True


class Tools(commands.Cog):
    def __init__(self, bot: Rift):
        self.bot = bot

    @commands.group(name="tools", type=commands.CommandType.chat_input)
    async def tools(self, ctx: RiftContext):
        ...

    @tools.command(  # type: ignore
        name="infrastructure",
        brief="Calculates infrastructure cost.",
        type=commands.CommandType.chat_input,
        descriptions={
            "before": "The starting infrastructure.",
            "after": "The final infrastructure.",
            "urbanization_policy": "Whether or not the Urbanization policy should be accounted for.",
            "center_for_civil_engineering": "Whether or not the Center for Civil Engineering project should be accounted for.",
            "advanced_engineering_corps": "Whether or not the Advanced Engineering Corps project should be accounted for.",
        },
    )
    async def tools_infrastructure(
        self,
        ctx: RiftContext,
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

    @tools.command(  # type: ignore
        name="land",
        brief="Calculates land cost.",
        type=commands.CommandType.chat_input,
        descriptions={
            "before": "The starting land.",
            "after": "The final land.",
            "rapid_expansion_policy": "Whether or not the Rapid Expansion policy should be accounted for.",
            "arable_land_agency": "Whether or not the Arable Land Agency project should be accounted for.",
            "advanced_engineering_corps": "Whether or not the Advanced Engineering Corps project should be accounted for.",
        },
    )
    async def tools_land(
        self,
        ctx: RiftContext,
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

    @tools.command(  # type: ignore
        name="city",
        brief="Calculates city cost.",
        type=commands.CommandType.chat_input,
        descriptions={
            "before": "The starting city.",
            "after": "The final city.",
            "manifest_destiny_policy": "Whether or not the Manifest Destiny policy should be accounted for.",
            "urban_planning": "Whether or not the Urban Planning project should be accounted for.",
            "advanced_urban_planning": "Whether or not the Advanced Urban Planning project should be accounted for.",
        },
    )
    async def tools_city(
        self,
        ctx: RiftContext,
        before: int,
        after: int,
        manifest_destiny_policy: bool = False,
        urban_planning: bool = False,
        advanced_urban_planning: bool = False,
    ):
        if before < 1:
            return await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    "Sorry, but I can't calculate that range of cities! I can only calculate numbers above 1.",
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

    @tools.group(name="nation", type=commands.CommandType.chat_input)  # type: ignore
    async def tools_nation(self, ctx: RiftContext):
        ...

    @tools_nation.command(  # type: ignore
        name="infrastructure",
        brief="Calculate infrastructure cost for a nation.",
        type=commands.CommandType.chat_input,
        descriptions={
            "after": "The final infrastructure.",
            "nation": "The nation to calculate for, defaults to your nation.",
            "only_buy": "Whether to only buy as opposed to selling excess, defaults to selling.",
        },
    )
    async def tools_nation_infrastructure(
        self,
        ctx: RiftContext,
        after: float,
        nation: Nation = MISSING,
        only_buy: bool = False,
    ):
        nation = nation or await Nation.convert(ctx, nation)
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
            if check_after(i.infrastructure, after, only_buy)
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

    @tools_nation.command(  # type: ignore
        name="land",
        brief="Calculate land cost for a nation.",
        type=commands.CommandType.chat_input,
        descriptions={
            "after": "The final land.",
            "nation": "The nation to calculate for, defaults to your nation.",
            "only_buy": "Whether to only buy as opposed to selling excess, defaults to selling.",
        },
    )
    async def tools_nation_land(
        self,
        ctx: RiftContext,
        after: float,
        nation: Nation = MISSING,
        only_buy: bool = False,
    ):
        nation = nation or await Nation.convert(ctx, nation)
        if any(after - i.land >= 1000000 for i in nation.partial_cities):
            return await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    "Sorry, but I can't calculate that much land!",
                    color=discord.Color.red(),
                )
            )
        raw_cost = cost = sum(
            funcs.calculate_land_value(i.land, after)
            for i in nation.partial_cities
            if check_after(i.land, after, only_buy)
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

    @tools_nation.command(  # type: ignore
        name="city",
        brief="Calculate city cost for a nation.",
        type=commands.CommandType.chat_input,
        descriptions={
            "after": "The final city.",
            "nation": "The nation to calculate for, defaults to your nation.",
        },
    )
    async def tools_nation_city(
        self,
        ctx: RiftContext,
        after: int,
        nation: Nation = MISSING,
    ):
        nation = nation or await Nation.convert(ctx, nation)
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

    @tools.group(name="alliance", type=commands.CommandType.chat_input)  # type: ignore
    async def tools_alliance(self, ctx: RiftContext):
        ...

    @tools_alliance.command(  # type: ignore
        name="infrastructure",
        brief="Calculate infrastructure cost for an alliance.",
        type=commands.CommandType.chat_input,
        descriptions={
            "after": "The final infrastructure.",
            "alliance": "The alliance to calculate for, defaults to your alliance.",
            "only_buy": "Whether to only buy as opposed to selling excess, defaults to selling.",
        },
    )
    async def tools_alliance_infrastructure(
        self,
        ctx: RiftContext,
        after: float,
        alliance: Alliance = MISSING,
        only_buy: bool = False,
    ):
        alliance = alliance or await Alliance.convert(ctx, alliance)
        if any(after - i.infrastructure >= 1000000 for i in alliance.partial_cities):
            return await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    "Sorry, but I can't calculate that much infrastructure!",
                    color=discord.Color.red(),
                )
            )
        await ctx.interaction.response.defer()
        projects = (
            await pnwkit.async_alliance_query(
                {"id": alliance.id, "first": 1},
                {"nations": ["id", "cfce", "adv_engineering_corps"]},
            )
        )[0]
        projects = {int(i.id): i for i in projects.nations}
        total_cost = 0
        for nation in alliance.members:
            projs = projects.get(nation.id)
            if projs is None:
                continue
            raw_cost = cost = sum(
                funcs.calculate_infrastructure_value(i.infrastructure, after)
                for i in nation.partial_cities
                if check_after(i.infrastructure, after, only_buy)
            )
            if nation.domestic_policy == "Urbanization":
                cost -= raw_cost * 0.05
            if projs.cfce:
                cost -= raw_cost * 0.05
            if projs.adv_engineering_corps:
                cost -= raw_cost * 0.05
            total_cost += cost
        await ctx.edit(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"The cost to buy all cities of {repr(alliance)} to {after:,.2f} infrastructure is ${total_cost:,.2f}.",
                color=discord.Color.green(),
            )
        )

    @tools_alliance.command(  # type: ignore
        name="land",
        brief="Calculate land cost for an alliance.",
        type=commands.CommandType.chat_input,
        descriptions={
            "after": "The final land.",
            "alliance": "The alliance to calculate for, defaults to your alliance.",
            "only_buy": "Whether to only buy as opposed to selling excess, defaults to selling.",
        },
    )
    async def tools_alliance_land(
        self,
        ctx: RiftContext,
        after: float,
        alliance: Alliance = MISSING,
        only_buy: bool = False,
    ):
        alliance = alliance or await Alliance.convert(ctx, alliance)
        if any(after - i.infrastructure >= 1000000 for i in alliance.partial_cities):
            return await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    "Sorry, but I can't calculate that much land!",
                    color=discord.Color.red(),
                )
            )
        await ctx.interaction.response.defer()
        projects = (
            await pnwkit.async_alliance_query(
                {"id": alliance.id, "first": 1},
                {"nations": ["id", "arable_land_agency", "adv_engineering_corps"]},
            )
        )[0]
        projects = {int(i.id): i for i in projects.nations}
        total_cost = 0
        for nation in alliance.members:
            projs = projects.get(nation.id)
            if projs is None:
                continue
            raw_cost = cost = sum(
                funcs.calculate_land_value(i.land, after)
                for i in nation.partial_cities
                if check_after(i.land, after, only_buy)
            )
            if nation.domestic_policy == "Rapid Expansion":
                cost -= raw_cost * 0.05
            if projs.arable_land_agency:
                cost -= raw_cost * 0.05
            if projs.adv_engineering_corps:
                cost -= raw_cost * 0.05
            total_cost += cost
        await ctx.edit(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"The cost to buy all cities of {repr(alliance)} to {after:,.2f} land is ${total_cost:,.2f}.",
                color=discord.Color.green(),
            )
        )

    @tools_alliance.command(  # type: ignore
        name="city",
        brief="Calculate city cost for an alliance.",
        type=commands.CommandType.chat_input,
        descriptions={
            "after": "The final city.",
            "alliance": "The alliance to calculate for, defaults to your alliance.",
        },
    )
    async def tools_alliance_city(
        self,
        ctx: RiftContext,
        after: int,
        alliance: Alliance = MISSING,
    ):
        alliance = alliance or await Alliance.convert(ctx, alliance)
        await ctx.interaction.response.defer()
        projects = (
            await pnwkit.async_alliance_query(
                {"id": alliance.id, "first": 1},
                {"nations": ["id", "uap", "adv_city_planning"]},
            )
        )[0]
        projects = {int(i.id): i for i in projects.nations}
        total_cost = 0
        for nation in alliance.members:
            if nation.cities >= after:
                continue
            projs = projects.get(nation.id)
            if projs is None:
                continue
            raw_cost = cost = funcs.calculate_city_value(nation.cities, after)
            if projs.uap:
                cost -= 50000000 * (after - nation.cities)
            if projs.adv_city_planning:
                cost -= 100000000 * (after - nation.cities)
            if nation.domestic_policy == "Manifest Destiny":
                cost -= raw_cost * 0.05
            total_cost += cost
        await ctx.edit(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"The cost to buy all nations of {repr(alliance)} to city {after} is ${total_cost:,.2f}.",
                color=discord.Color.green(),
            )
        )


def setup(bot: Rift):
    bot.add_cog(Tools(bot))
