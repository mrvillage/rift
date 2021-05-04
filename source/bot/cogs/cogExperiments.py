import discord
from discord.ext import commands

from ...data.query import get_mmr  # pylint: disable=relative-beyond-top-level


class Experiments(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="mmr")
    async def mmr(self, ctx):
        print(await get_mmr(mmr_id=1))


def setup(bot):
    bot.add_cog(Experiments(bot))