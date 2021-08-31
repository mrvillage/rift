from __future__ import annotations

from discord.ext import commands

from ...ref import Rift


class Fun(commands.Cog):
    def __init__(self, bot: Rift):
        self.bot = bot

    @commands.command(name="toot")
    async def toot(self, ctx: commands.Context):
        await ctx.send("Toot tooooooot!")


def setup(bot: Rift):
    bot.add_cog(Fun(bot))
