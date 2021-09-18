from __future__ import annotations

import discord
from discord.ext import commands

from ... import Rift
from ...data.classes import Nation
from ...ref import Rift


class Tools(commands.Cog):
    def __init__(self, bot: Rift):
        self.bot = bot

    @commands.group(name="tools", type=commands.CommandType.chat_input)
    async def tools(self, ctx: commands.Context):
        ...

    @tools.command(name="infrastructure", type=commands.CommandType.chat_input)
    async def tools_infrastructure(self, ctx: commands.Context, *, before: float, after: float, urbanization_policy: bool = False, center_for_civil_engineering: bool = False, advanced_engineering_corps: bool = False):
        ...

    @tools.command(name="land", type=commands.CommandType.chat_input)
    async def tools_land(self, ctx: commands.Context, *, before: float, after: float, rapid_expansion_policy: bool = False, arable_land_agency: bool = False, advanced_engineering_corps: bool = False):
        ...

    @tools.command(name="city", type=commands.CommandType.chat_input)
    async def tools_city(self, ctx: commands.Context, *, before: int, after: int, manifest_destiny_policy: bool = False, urban_planning: bool = False, advanced_urban_planning: bool = False):
        ...

    @tools.group(name="nation", type=commands.CommandType.chat_input)
    async def tools_nation(self, ctx: commands.Context):
        ...

    @tools.command(name="infrastructure", type=commands.CommandType.chat_input)
    async def tools_nation_infrastructure(self, ctx: commands.Context, *, nation: Nation, after: float):
        ...

    @tools.command(name="land", type=commands.CommandType.chat_input)
    async def tools_nation_land(self, ctx: commands.Context, *, nation: Nation, after: float):
        ...

    @tools.command(name="city", type=commands.CommandType.chat_input)
    async def tools_nation_city(self, ctx: commands.Context, *, nation: Nation, after: int):
        ...

def setup(bot: Rift):
    bot.add_cog(Tools(bot))
