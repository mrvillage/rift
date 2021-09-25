from __future__ import annotations

import inspect
from io import BytesIO
from typing import TYPE_CHECKING

import aiohttp
import discord
import pnwkit
from discord.ext import commands

from ... import find, funcs
from ...data.classes import Alliance, Nation
from ...errors import AllianceNotFoundError, NationNotFoundError


class Military(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(
        name="militarization",
        aliases=["m", "mil", "military"],
        brief="A group of commands related to militarization, defaults to alliance.",
        case_insensitive=True,
        invoke_without_command=True,
        type=(commands.CommandType.default, commands.CommandType.chat_input),
        descriptions={"alliance": "The alliance to check the militarization of."},
    )
    async def militarization(self, ctx: commands.Context, *, alliance: Alliance = None):
        alliance = alliance or await Alliance.convert(ctx, alliance)
        if ctx.interaction:
            await ctx.interaction.response.defer()
            async with aiohttp.request(
                "GET", f"https://checkapi.bsnk.dev/getChart?allianceID={alliance.id}"
            ) as req:
                byte = await req.read()
        else:
            async with ctx.typing():
                async with aiohttp.request(
                    "GET",
                    f"https://checkapi.bsnk.dev/getChart?allianceID={alliance.id}",
                ) as req:
                    byte = await req.read()
        militarization = alliance.get_militarization(vm=False)
        image = discord.File(BytesIO(byte), f"militarization_{alliance.id}.png")
        cities = alliance.get_cities()
        alliance_data = await pnwkit.async_alliance_query(
            {"id": alliance.id, "first": 1},
            {
                "nations": [
                    "alliance_position",
                    {"cities": ["barracks", "factory", "airforcebase", "drydock"]},
                ]
            },
        )
        if TYPE_CHECKING:
            assert isinstance(alliance_data, tuple)
        nations = [
            i
            for i in alliance_data[0].nations
            if i.alliance_position not in {"NOALLIANCE", "APPLICANT"}
        ]
        improvements = {
            "barracks": sum(
                sum(city.barracks for city in nation.cities) / len(nation.cities)
                for nation in nations
            )
            / len(nations),
            "factories": sum(
                sum(city.factory for city in nation.cities) / len(nation.cities)
                for nation in nations
            )
            / len(nations),
            "hangars": sum(
                sum(city.airforcebase for city in nation.cities) / len(nation.cities)
                for nation in nations
            )
            / len(nations),
            "drydocks": sum(
                sum(city.drydock for city in nation.cities) / len(nation.cities)
                for nation in nations
            )
            / len(nations),
        }
        embed = funcs.get_embed_author_member(
            ctx.author,
            inspect.cleandoc(
                f"""
            Total Militarization: {militarization['total']*100:.2f}%
            Soldier Militarization: {militarization['soldiers']*100:.2f}% ({improvements['barracks']:,.3f} Barracks)
            Tank Militarization: {militarization['tanks']*100:.2f}% ({improvements['factories']:,.3f} factories)
            Aircraft Militarization: {militarization['aircraft']*100:.2f}% ({improvements['hangars']:,.3f} Hangars)
            Ship Militarization: {militarization['ships']*100:.2f}% ({improvements['drydocks']:,.3f} Drydocks)
            """
            ),
            title=f"Militarization Graph for {alliance.name} (`{alliance.id}`)",
            image_url=f"attachment://militarization_{alliance.id}.png",
            fields=[
                {
                    "name": "Soldiers",
                    "value": f"{alliance.get_soldiers():,}/{cities*15000:,}",
                },
                {"name": "Tanks", "value": f"{alliance.get_tanks():,}/{cities*1250:,}"},
                {
                    "name": "Aircraft",
                    "value": f"{alliance.get_aircraft():,}/{cities*75:,}",
                },
                {"name": "Ships", "value": f"{alliance.get_ships():,}/{cities*15:,}"},
                {"name": "Missiles", "value": f"{alliance.get_missiles():,}"},
                {"name": "Nukes", "value": f"{alliance.get_nukes():,}"},
            ],
            color=discord.Color.blue(),
        )
        await ctx.reply(file=image, embed=embed)

    @commands.command(name="militarization-nation", aliases=["mn"], hidden=True)
    async def mn_shortcut(self, ctx: commands.Context, *, nation: Nation = None):
        await ctx.invoke(self.militarization_nation, nation=nation)

    @militarization.command(
        name="alliance",
        aliases=["m", "aa"],
        brief="Get the militarization of an alliance.",
        type=(commands.CommandType.default, commands.CommandType.chat_input),
        descriptions={"alliance": "The alliance to check the militarization of."},
    )
    async def militarization_alliance(
        self, ctx: commands.Context, *, alliance: Alliance = None
    ):
        await ctx.invoke(self.militarization, alliance=alliance)

    @militarization.command(
        name="nation",
        aliases=["n", "nat", "me"],
        brief="Get the militarization of a nation.",
        type=(commands.CommandType.default, commands.CommandType.chat_input),
        descriptions={"nation": "The nation to check the militarization of."},
    )
    async def militarization_nation(self, ctx, *, nation: Nation = None):
        nation = nation or await Nation.convert(ctx, nation)
        author = nation.user or ctx.author
        militarization = nation.get_militarization()
        nation_data = await pnwkit.async_nation_query(
            {"id": nation.id},
            {"cities": ["barracks", "factory", "airforcebase", "drydock"]},
        )
        if TYPE_CHECKING:
            assert isinstance(nation_data, tuple)
        improvements = {
            "barracks": sum(city.barracks for city in nation_data[0].cities)
            / nation.cities,
            "factories": sum(city.factory for city in nation_data[0].cities)
            / nation.cities,
            "hangars": sum(city.airforcebase for city in nation_data[0].cities)
            / nation.cities,
            "drydocks": sum(city.drydock for city in nation_data[0].cities)
            / nation.cities,
        }
        if isinstance(author, discord.Guild):
            embed = funcs.get_embed_author_guild(
                author,
                inspect.cleandoc(
                    f"Total Militarization: {militarization['total']*100:.2f}%\nSoldier Militarization: {militarization['soldiers']*100:.2f}% ({improvements['barracks']:,.2f} Barracks)\nTank Militarization: {militarization['tanks']*100:.2f}% ({improvements['factories']:,.2f} Factories)\nAircraft Militarization: {militarization['aircraft']*100:.2f}% ({improvements['hangars']:,.2f} Hangars)\nShip Militarization: {militarization['ships']*100:.2f}% ({improvements['drydocks']:,.2f} Drydocks)"
                ),
                title=f"Militarization for {nation.name} (`{nation.id}`)",
                fields=[
                    {
                        "name": "Soldiers",
                        "value": f"{nation.soldiers:,}/{nation.cities*15000:,}",
                    },
                    {
                        "name": "Tanks",
                        "value": f"{nation.tanks:,}/{nation.cities*1250:,}",
                    },
                    {
                        "name": "Aircraft",
                        "value": f"{nation.aircraft:,}/{nation.cities*75:,}",
                    },
                    {
                        "name": "Ships",
                        "value": f"{nation.ships:,}/{nation.cities*15:,}",
                    },
                    {"name": "Missiles", "value": f"{nation.missiles:,}"},
                    {"name": "Nukes", "value": f"{nation.nukes:,}"},
                ],
                color=discord.Color.blue(),
            )
        else:
            embed = funcs.get_embed_author_member(
                author,
                f"Total Militarization: {militarization['total']*100:.2f}%\nSoldier Militarization: {militarization['soldiers']*100:.2f}% ({improvements['barracks']:,.2f} Barracks)\nTank Militarization: {militarization['tanks']*100:.2f}% ({improvements['factories']:,.2f} Factories)\nAircraft Militarization: {militarization['aircraft']*100:.2f}% ({improvements['hangars']:,.2f} Hangars)\nShip Militarization: {militarization['ships']*100:.2f}% ({improvements['drydocks']:,.2f} Drydocks)",
                title=f"Militarization for {nation.name} (`{nation.id}`)",
                fields=[
                    {
                        "name": "Soldiers",
                        "value": f"{nation.soldiers:,}/{nation.cities*15000:,}",
                    },
                    {
                        "name": "Tanks",
                        "value": f"{nation.tanks:,}/{nation.cities*1250:,}",
                    },
                    {
                        "name": "Aircraft",
                        "value": f"{nation.aircraft:,}/{nation.cities*75:,}",
                    },
                    {
                        "name": "Ships",
                        "value": f"{nation.ships:,}/{nation.cities*15:,}",
                    },
                    {"name": "Missiles", "value": f"{nation.missiles:,}"},
                    {"name": "Nukes", "value": f"{nation.nukes:,}"},
                ],
                color=discord.Color.blue(),
            )
        await ctx.reply(embed=embed)


def setup(bot):
    bot.add_cog(Military(bot))
