from __future__ import annotations

import discord
from discord.ext import commands

from ...ref import Rift


class Tickets(commands.Cog):
    def __init__(self, bot: Rift):
        self.bot = bot

    @commands.group(name="ticket")
    @commands.guild_only()
    async def ticket(self, ctx: commands.Context):
        ...


def setup(bot: Rift) -> None:
    bot.add_cog(Tickets(bot))
